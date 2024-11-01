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
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.factory import Factory as F
import asynckivy as ak
from kivy_garden.draggable import KXDraggableBehavior


@dataclass
class task_to_be_done:
    name: str = ''
    time: int = 0
    energy: int = 0
    texture: F.Texture = None


class SharingApp(App):
    def build(self):
        Builder.load_file('task_manager.kv')
        return SHMain()

    def on_start(self):
        ak.start(self.root.main(db_path=__file__ + r".sqlite3"))


class SHMain(F.BoxLayout):
    def show_total(self, *, _cache=[]):
        try:
            popup = _cache.pop()
        except IndexError:
            popup = F.Popup(
                size_hint=(.5, .2, ),
                title='Total',
                content=F.Label(),
            )
            popup.bind(on_dismiss=lambda popup, _cache=_cache: _cache.append(popup))
        total_time = sum(d.time for d in self.ids.cart.data)
        total_energy= sum(d.energy for d in self.ids.cart.data)
        popup.content.text = f"{total_time} hours / {total_energy} energy bar " 
        popup.open()

    async def main(self, db_path: PathLike):
        from random import randint
        from io import BytesIO
        from kivy.core.image import Image as CoreImage
        conn = await self._load_database(db_path)
        with closing(conn.cursor()) as cur:
            # FIXME: It's probably better to ``Texture.add_reload_observer()``.
            self.task_textures = textures = {
                name: CoreImage(BytesIO(open(image_path,"rb").read()), ext='png').texture
                for name, image_path in cur.execute("SELECT name, image_path FROM Tasks")
            }
            self.ids.shelf.data = [
                task_to_be_done(name=name, time=time, energy=energy,  texture=textures[name])
                for name, time, energy in cur.execute("SELECT name, time, energy FROM Tasks")
            ]

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
            cur.executescript("""
                CREATE TABLE Tasks (
                    name TEXT NOT NULL UNIQUE,
                    time INT NOT NULL,
                    energy INT NOT NULL,
                    image_path TEXT NOT NULL,
                    PRIMARY KEY (name)
                );
                INSERT INTO Tasks(name, time, energy, image_path) VALUES                
                    ('Cooking', 3, 3, 'assets/cooking.png'),
                    ('Cleaning', 3, 5 , 'assets/mop.png'),
                    ('Essentials', 2, 2 , 'assets/vegetable.png'),
                    ('Child-care', 7,7 , 'assets/crawl.png'),
                    ('Elderly-care', 7,7 , 'assets/elderly.png'),
                    ('Other Care', 7,7, 'assets/care.png');
            """)


class SHTask(KXDraggableBehavior, F.BoxLayout):
    datum = ObjectProperty(task_to_be_done(), rebind=True)


class EquitableBoxLayout(F.BoxLayout):
    '''Always dispatches touch events to all its children'''
    def on_touch_down(self, touch):
        return any([c.dispatch('on_touch_down', touch) for c in self.children])
    def on_touch_move(self, touch):
        return any([c.dispatch('on_touch_move', touch) for c in self.children])
    def on_touch_up(self, touch):
        return any([c.dispatch('on_touch_up', touch) for c in self.children])


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