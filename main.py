'''
Reference video : https://www.youtube.com/watch?v=PNj8uEdd5c0
Reference code : https://github.com/kivy-garden/draggable/blob/main/examples/shopping.py
Reference about unpaid work : https://www.unwomen.org/sites/default/files/2022-06/A-toolkit-on-paid-and-unpaid-care-work-en.pdf
'''

import itertools
from contextlib import closing
from os import PathLike
import sqlite3
from typing import Tuple, Iterable
from dataclasses import dataclass
from kivy.app import App
from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.factory import Factory as F
import asynckivy as ak
from kivy_garden.draggable import KXDraggableBehavior, KXReorderableBehavior
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from gemini_calls import generate_game_scenario
from sql_queries import CHOOSE_COUPLE_SQL, CREATE_TABLES, get_texture
from types import SimpleNamespace
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window

@dataclass
class task_to_be_done:
    name: str = ''
    energy: int = 0
    texture: F.Texture = None

class CircularProgresBar(AnchorLayout):
    set_value = NumericProperty(2)
    bar_color = ListProperty([1,0,100/255,.1])
    bar_width = NumericProperty(10)

class SharingApp(App):
    def build(self):
        Builder.load_file('task_manager.kv')
        return SHMain()

    def on_start(self):
        ak.start(self.root.main(db_path=__file__ + r".sqlite3"))

    def restart(self):
        self.root.clear_widgets()
        self.on_stop()
        self.on_start()

class EquitableBoxLayout(F.BoxLayout):
    '''Always dispatches touch events to all its children'''
    def on_touch_down(self, touch):
        return any([c.dispatch('on_touch_down', touch) for c in self.children])
    def on_touch_move(self, touch):
        return any([c.dispatch('on_touch_move', touch) for c in self.children])
    def on_touch_up(self, touch):
        return any([c.dispatch('on_touch_up', touch) for c in self.children])

class SHMain(F.BoxLayout):
    prompt = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._equality_text = None

    def my_sum_callback(self, dt):
        try:
            self.ids.male_details.energy = sum([data.energy for data in self.ids.man.data]) 
            self.ids.female_details.energy = sum([data.energy for data in self.ids.woman.data])
        except Exception as ex:
            print(ex)

    def _unpack_couple_names(self,couple_names, actor):
        self.ids.male_details.name = couple_names['man']['name']
        self.ids.male_details.energy = couple_names['man']['energy']
        self.ids.female_details.name = couple_names['woman']['name']
        self.ids.female_details.energy = couple_names['man']['energy']
        self.ids.male_details.source = actor[1]
        self.ids.female_details.source = actor[3]

    def generate_prompt(self, conn):
        with closing(conn.cursor()) as cur:
            actor =  [(male_name, male_image_path, female_name, female_image_path) for (male_name, male_image_path, female_name, female_image_path) in  cur.execute(CHOOSE_COUPLE_SQL)][0]
            tasks_to_complete = [
                task_to_be_done(name=name, energy=energy,  texture=None)
                for name, energy in cur.execute("SELECT name, energy FROM Tasks")
            ]
            game_scenario = generate_game_scenario(tasks_to_complete)
            self.ids.prompt_text.text += game_scenario["background_story"]
            self._unpack_couple_names(game_scenario['couple_names'], actor)
            return game_scenario

    def show_total(self,total_energy, *, _cache=[]):
        try:
            popup = _cache.pop()
        except IndexError:
            popup = F.Popup(
                size_hint=(.5, .2, ),
                title='Total',
                content=F.Label(),
            )
            popup.bind(on_dismiss=lambda popup, _cache=_cache: _cache.append(popup))
        popup.content.text = f"{total_energy} energy bar " 
        popup.open()

    def show_message(self, *, _cache=[]):
        try:
            popup = _cache.pop()
        except IndexError:
            popup = F.Popup(
                title='Gender Equality',
                content=F.Label(),
                size_hint=(1, .2),
            )
            popup.bind(on_dismiss=lambda popup, _cache=_cache: _cache.append(popup))
        popup.content.text = self._equality_text
        popup.open()

    async def main(self, db_path: PathLike):
        from random import randint
        from io import BytesIO
        from kivy.core.image import Image as CoreImage
        conn = await self._load_database(db_path)
        game_scenario = self.generate_prompt(conn)
        self._equality_text = game_scenario['equality_fact']
        sampled_chores, renamed = game_scenario['list_of_chores'], game_scenario['renamed'][0]

        with closing(conn.cursor()) as cur:
            # FIXME: It's probably better to ``Texture.add_reload_observer()``.
            set_of_names = set(SimpleNamespace(**task).name for task in sampled_chores)
          
            for new_value, og_value in renamed.items():
                set_of_names.discard(new_value)
                set_of_names.add(og_value)

            names_tuple = tuple(set_of_names)

            self.task_textures = textures = {
                name: CoreImage(BytesIO(open(image_path,"rb").read()), ext='png').texture
                for name, image_path in cur.execute(get_texture(names_tuple))
            }

            final_list = []
            for task_dict in sampled_chores:
                task =  SimpleNamespace(**task_dict) 
                if task.name in set_of_names:
                    final_list.append(task_to_be_done(name=task.name, energy=task.energy_to_be_spent, texture=self.task_textures[task.name]))
                else:
                    final_list.append(task_to_be_done(name=task.name, energy=task.energy_to_be_spent, texture=self.task_textures[renamed[task.name]]))

            self.ids.shelf.data = final_list

        Clock.schedule_interval(self.my_sum_callback, 1)


    @staticmethod
    async def _load_database(db_path: PathLike) -> sqlite3.Connection:
        from os.path import exists
        already_exists = exists(db_path)
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        if not already_exists:
            try:
                await SHMain._init_database(conn)
            except Exception:
                from os import remove
                remove(db_path)
                raise
            else:
                conn.commit()
        return conn

    @staticmethod
    async def _init_database(conn: sqlite3.Connection):
        from concurrent.futures import ThreadPoolExecutor
        import requests
        import asynckivy as ak
        with closing(conn.cursor()) as cur:
            cur.executescript(CREATE_TABLES)


class SHTask(KXDraggableBehavior, F.BoxLayout):
    datum = ObjectProperty(task_to_be_done(), rebind=True)

        
class RVLikeBehavior:
    '''Mix-in class that adds RecyclewView-like interface to layouts. But
    unlike RecycleView, this one creates view widgets as much as the number
    of the data.
    '''

    viewclass = ObjectProperty()
    '''widget-class or its name'''

    def __init__(self, **kwargs):
        self._rv_refresh_params = {}
        self._rv_trigger_refresh = Clock.create_trigger(self._rv_refresh, -1)
        super().__init__(**kwargs)

    def on_viewclass(self, *args):
        self._rv_refresh_params['viewclass'] = None
        self._rv_trigger_refresh()

    def _get_data(self) -> Iterable:
        data = self._rv_refresh_params.get('data')
        return [c.datum for c in reversed(self.children)] if data is None else data

    def _set_data(self, new_data: Iterable):
        self._rv_refresh_params['data'] = new_data
        self._rv_trigger_refresh()

    data = property(_get_data, _set_data)

    def _rv_refresh(self, *args):
        viewclass = self.viewclass
        if not viewclass:
            self.clear_widgets()
            return
        data = self.data
        params = self._rv_refresh_params
        reusable_widgets = '' if 'viewclass' in params else self.children[::-1]
        self.clear_widgets()
        if isinstance(viewclass, str):
            viewclass = F.get(viewclass)
        for datum, w in zip(data, itertools.chain(reusable_widgets, iter(viewclass, None))):
            w.datum = datum
            self.add_widget(w)
        params.clear()
F.register('RVLikeBehavior', cls=RVLikeBehavior)


if __name__ == '__main__':
    SharingApp().run()