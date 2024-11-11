# Project Story: Let's Do This Together

By putting players in the shoes of someone managing household responsibilities, the project highlights the often unseen work of caregiving. I hope players walk away with a better understanding of the need for shared responsibilities, fostering more equitable mindsets in their own lives.

## Inspiration

Among the powerful goals within **UN SDG-5** (Gender Equality), the advocacy for recognizing and valuing unpaid care and domestic work, and promoting shared responsibilities, resonated deeply with me. As a South Asian, I’ve been fortunate to have a family that encouraged me to see beyond gender-based limitations. This project is a tribute to my mother and countless others like her who bravely carry the weight of household responsibilities. It’s my way of saying, "*We see you, we thank you, and we are committed to sharing the load.*"

## What It Does

Building on insights from previous hackathons, I realized how effective games can be in breaking down complex social concepts. I wanted to create a game that could both educate and foster empathy around the often invisible work of household caregiving.

In the game, players are introduced to a couple and their background story, then presented with a list of household chores to be divided. The player drags and drops images of chores next to either the man or the woman, aiming to distribute the workload equally. At any point, the player can click the **“Complete Story”** button, generating an ending to the story based on the player’s choices. They can adjust chores and regenerate a story to see a different outcome or start a new scenario with a new couple.

This interactive setup lets players see the impact of shared responsibilities and helps them understand the value of equitable partnerships in everyday life.

## How I Built the Project

The project was brought to life using:

- **Kivy** for building the interactive game interface.
- **Gemini API** to add narrative depth, dynamically generating story endings based on chore distribution.
- **Gemini as a resource for debugging and brainstorming** throughout development.
- **Gemini AI Studio** to test prompts and develop game elements.
- **Python** as the primary programming language.

Each step involved integrating Gemini’s AI capabilities to generate unique storylines and character interactions, making the game feel responsive to the player’s decisions. This approach immerses players in real-life scenarios, encouraging them to reflect on the significance of sharing household responsibilities.

# Prerequisites
- **Operating System**: Developed on MacOS 14.4.1, but it may work on other operating systems.
- **Python Version**: Requires **Python 3.11.10**. Ensure this version or higher is installed.
- **Environment Variable**: Requires a `GEMINI_API_KEY` (see Running the Application section).
- **Libraries**: Install dependencies using the provided `requirements.txt` file.

## Download Link
Clone or download the repository from GitHub:
```bash
git clone https://github.com/Sahanave/she-builds-ai-sdg-5
cd she-builds-ai-sdg-5
```

## Installation Instructions
Install required libraries with the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

## Running the Application
To start the application, run the following command, replacing `'your_actual_key'` with your actual Gemini API key:
```bash
GEMINI_API_KEY='your_actual_key' python main.py
```

## Troubleshooting
- **API Key Error**: If you encounter an error related to `GEMINI_API_KEY`, verify the key and that it is properly set in the command.
- **OS Compatibility**: If issues arise on non-Linux systems, consider testing in a Linux environment.

## References
- Icon made by authors from www.flaticon.com.
- Background was downloded from 
    - https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRfiBefc9OBdYbPd58cq0uIS2tUJsYDU4wKIA&s
    - https://wallcoveringsmart.com/cdn/shop/products/343276.jpg?v=1607876577

