ROLE_PROMPT="""
You are an expert advisor in everything about Minecraft and its mods.
When system asks you about outputting something, like number, single string, dictionary and other precise data - output only it without any explanation or wrapping,
as it will be used to determine next steps in the langgraph.
"""


unsuccessful_determination_placeholder = 0

DETERMINE_QUERY_SUBJECT_PROMPT=f"""
Based on users query and chat history, determine subject of users query.
For example: in query "how to craft stone sword", subject is "stone sword", not the performed action.
Subject may be modified with some extra information, like "Tier 4 blood altar", this whole thing will be the subject. 
If there is no subject in query, try to find subject in the latest messages from user in chat history, if found subject - output subject, otherwise output '{unsuccessful_determination_placeholder}'.
"""


answer_exists_placeholder = 1
answer_does_not_exists_placeholder = 0

ANSWER_EXISTS_IN_CHAT_HISTORY_PROMPT=f"""
You are an AI assistant tasked with determining whether a potential answer in the chat history strictly addresses the user's current query.

Instructions:
1. Review the user's current query and the chat history.
2. If you find a response in the chat history that directly and fully answers the user's query, output '{answer_exists_placeholder}'.
3. If no such response exists, output '{answer_does_not_exists_placeholder}'.
"""

FIND_ANSWER_IN_CHAT_HISTORY_PROMPT=f"""
You are an AI assistant tasked with determining whether a potential answer in the chat history strictly addresses the user's current query.

Instructions:
1. Review the user's current query and the chat history.
2. If you find a response in the chat history that directly and fully answers the user's query, output the answer without any explanation or wrapping.
3. If no such response exists, output '{answer_does_not_exists_placeholder}'.
"""


query_is_about_looks_placeholder = 1
query_is_not_about_looks_placeholder = 0

DETERMINE_IF_QUERY_IS_ABOUT_LOOKS_PROMPT=f"""
You are an AI assistant tasked with determining whether users query is about how something looks.

Instructions:
1. Review the user's current query and the chat history.
2. If users query is about how something looks, output '{query_is_about_looks_placeholder}', otherwise output '{query_is_not_about_looks_placeholder}'.
"""


query_topic_is_craft_placeholder = 1
query_topic_is_building_placeholder = 2
query_topic_is_summoning_placeholder = 3
query_topic_is_general_info_placeholder = 4

DETERMINE_QUERY_TOPIC_PROMPT=f"""
You are an AI assistant tasked with determining user's query topic.

Instructions:
1. Review the user's current query, its subject and the provided below context
subject: {{subject}}
context: {{context}} 
2. Select the most appropriate topic for user's query and the context:
    If topic is craft output: {query_topic_is_craft_placeholder}
    If topic is about building something: {query_topic_is_building_placeholder}
    If topic is summon: {query_topic_is_summoning_placeholder}
    If topic is any other: {query_topic_is_general_info_placeholder}
"""


REFINE_USER_QUERY_PROMPT="""
Based on user's query and provided subject, refine and output user's query as if user mentioned subject in his query.
subject: {subject}
"""


# General prompt - just for debug
ANSWER_QUERY_TOPIC="""
You are an AI assistant tasked with answering user's query.

Instructions:
1. Review the user's query, chat history and context
context: {context}
2. Output as concise and precise as possible answer for user's query
3. Answer can be deeply hidden in the context but i know you will find it!
"""


CRAFT_PROMPT="""
context: {context}

You are an AI assistant tasked with determining craft's recipe.

Instructions:
1. There maybe two versions of recipe in the context
2. Review the context and the query
3. If user just asked for the recipe - output original version of recipe.
4. If user clarified 
5. Extract the ingredients and their counts from the determined recipe.
6. Output the recipe in JSON format, where the ingredient is the key and the count is the value.
7. Provide only the JSON output, without any additional explanation or wrapping.
"""

context: Steps
  Part 1 Part 1 of 3: Making a Wooden Sword (Windows or Mac) Download Article 1 Gather wood. Hold down the left mouse button while your cursor is over a tree trunk. This will break the tree into wooden logs. The logs will automatically enter your inventory as long as you stand close to the tree. Repeat this several times. It does not matter whether you get oak wood, spruce wood, or any other type of wood. 2 Open your inventory. The default key for this is E. You should see a 2 x 2 grid next to your character picture. This is your crafting area. Advertisement 3 Drag the wood to the crafting area. Planks will appear in the results box to the right of the crafting area. Drag the planks to your inventory. You've now turned the wood into planks. 4 Make two wooden planks into sticks. Place one of the planks you just made on the lower row of the crafting area. Place a second plank directly above it. [1] X Research source Now you've made a bundle of sticks, which you should drag into your inventory from the results box. 5 Make a crafting table. Fill the entire 2 x 2 grid with planks to make a crafting table. Drag this to your quick slot bar at the base of your screen. Close your inventory and place the table on the ground. (To place a block, select it in your quick slot bar and right-click the ground.) Remember not to confuse planks and wood. Only planks will work for this recipe. 6 Open the crafting table. Right-click the table to open an expanded crafting interface. From here you can make recipes that require a 3 x 3 grid. 7 Craft the wooden sword. The sword recipe only fills a single column of the 3 x 3 grid. All ingredients must be in the same column, but it does not matter which column you choose: A plank on top A plank in the middle (directly below the first one) A stick at the base (directly below the planks) 8 Use the sword. Drag the sword to a quick slot and select it to equip it. Now left-clicking will use the sword instead of your hand. This is much more effective at killing enemies or animals, but be careful. A wooden sword is still pretty weak. Skip down to the section below on better swords if you want an upgrade. Advertisement Part 2 Part 2 of 3: Making a Wooden Sword (Consoles or Pocket Edition) Download Article 1 Turn trees into wood. You can break apart trees with your bare hands in Minecraft. In Pocket Edition, just hold your finger down over the tree and keep it there until it's turned into wood. On consoles, use the right trigger button. 2 Learn how to craft. Crafting is simple in these editions of Minecraft. The crafting menu has a list of available recipes, and you click the one you want. As long as you have the right ingredients, they will turn into the desired item. Here's how to get started: [2] X Research source In Pocket Edition, tap the icon with three dots at the bottom and select Craft. On Xbox, press X. On Playstation, press Square. On Xperia Play, press Select. 3 Make a crafting table. The crafting table gives you access to many more craftable items, including swords. Here's how to make one: With Wood in your inventory, craft Planks. With four Planks in your inventory, craft a Crafting Table. Select the Crafting Table in your quick bar and tap the ground to put it down. (Left trigger in console editions.) 4 Make the wooden sword. This is another multi-step process: With Wood in your inventory, make Planks. With two Planks in your inventory, make Sticks. With one Stick and two Planks in your inventory, make a Wooden Sword from the Tools crafting section. [3] X Research source 5 Use your sword. When you have a sword selected in your quick slot, tapping the screen or pressing the left trigger will swing your sword. This will hurt enemies and animals much more than your bare hands. Try jumping as you swing your sword. If you hit the target while you're falling (but not on the way up), you'll do a critical hit for 50% more damage. [4] X Research source Keep reading if you want to upgrade to a more damaging and durable sword. Advertisement Part 3 Part 3 of 3: Crafting Better Swords Download Article 1 Gather materials with a pickaxe. You'll need a pickaxe to gather the stone or metals for a better sword. [5] X Research source Here's a brief summary of how to find these, from most to least common: Stone is widely available in mountainsides and just beneath the surface. Mine it with a wooden pickaxe. Iron (stone with beige flecks) is fairly common just beneath the surface, and requires a stone pickaxe to mine. Gold and diamond ore are very rare and only found deep under the earth. 2 Craft a stone sword. Combine two cobblestone and a stick to make a stone sword. This deals 6 damage and lasts for 132 hits before breaking. (In comparison, the wooden sword does 5 damage and lasts for 60 hits.) [6] X Research source As with all swords, the computer recipe fills only one column, with the stick at the bottom. 3 Upgrade to iron. Iron is a great dependable material you'll be relying on for a long time. Once you have iron ingots (see below), you can make an iron sword that does 7 damage for 251 hits. After mining the ore, you'll need to smelt the iron ore into ingots using a furnace. 4 Make a golden sword for show. Despite its rarity, gold is not very good for tools. If you smelt the gold ingots and make them into a sword, it will deal the same damage as a wooden sword but only last for 33 hits. [7] X Research source There is one advantage to golden swords: they have the best chance at a high level enchantment . Many players still don't like to enchant them since they're such temporary tools. 5 Craft a diamond sword. Now you've really made it in the world. Diamonds are the best material for tools and weapons. They do not require smelting. A diamond sword does eight damage and lasts for 1,562 hits. [8] X Research source Diamonds occupy an important place in Minecraft because they help to create an enchanting table. [9] X Research source The table allows a player to add upgrades to their tools and armor. [10] X Research source 6 Repair your swords. Place two damaged swords of the same type anywhere in the crafting area. The result will be a sword with more durability than both of them put together. You cannot increase the durability past the sword's normal maximum this way. [11] X Research source A "damaged" sword is any sword that has been used at least once. You should see a small bar next to the item icon showing you how much durability is left. Advertisement Video Community Q&A Search Add New Question Question Why would you get two of the same kind of sword? CaptianYaya Community Answer This is how you get a higher durability on weapons, combining two of the same kind will double durability (and enchantments) to make a very powerful weapon. Thanks! We're glad this was helpful. Thank you for your feedback. If wikiHow has helped you, please consider a small contribution to support us in helping more readers like you. We’re committed to providing the world with free how-to resources, and even $1 helps us in our mission. Support wikiHow Yes No Not Helpful 6 Helpful 24 Question Which one is better: gold or diamond? QWERTY Community Answer Diamond. Thanks! We're glad this was helpful. Thank you for your feedback. If wikiHow has helped you, please consider a small contribution to support us in helping more readers like you. We’re committed to providing the world with free how-to resources, and even $1 helps us in our mission. Support wikiHow Yes No Not Helpful 23 Helpful 60 Question How do I use a bow and arrow? Community Answer Make sure you have arrows in your inventory. Place a bow in your hotba, and select it. "Use" it, and it will start to draw back. Once it zooms in while drawing back, it is at the highest possible power. Then release the "use" button and the arrow will fly toward your mark. You can usually tell at which height the arrow will hit by where the tip of it is pointing, which is usually above the crosshair. Thanks! We're glad this was helpful. Thank you for your feedback. If wikiHow has helped you, please consider a small contribution to support us in helping more readers like you. We’re committed to providing the world with free how-to resources, and even $1 helps us in our mission. Support wikiHow Yes No Not Helpful 22 Helpful 31 See more answers Ask a Question 200 characters left Include your email address to get a message when this question is answered. Submit Advertisement    Tips All damage and durability values given are for Minecraft 1.8. These values may change once 1.9 is released. [12] X Research source Thanks Helpful 0 Not Helpful 0 When fighting creepers, hit once, back up immediately, and repeat. This will usually avoid explosions. Thanks Helpful 1 Not Helpful 0 Some enemies have a chance to drop a sword, including wither skeletons and zombified piglins. This is usually far more effort than making your own, especially if you don't have a sword to fight with! Thanks Helpful 1 Not Helpful 0 Submit a Tip All tip submissions are carefully reviewed before being published Name Please provide your name and last initial Submit Thanks for submitting a tip for review! Advertisement      You Might Also Like How to Make Tools in Minecraft The Ultimate Guide to Making a Map in Minecraft How to Blow Up TNT in Minecraft How to Make an Armor Stand in Minecraft How to Make a TNT Cannon in Minecraft How to Make a Potion of Swiftness in Minecraft How to Make a Grindstone in Minecraft to Repair Your Tools How to Make a Book in Minecraft How to Use Enchanted Books in Minecraft How to Make Tripwire Hooks in Minecraft Craft and Use a Lantern in Minecraft: Step-by-Step Guide How to Make a Piston in Minecraft How to Make Colorful Concrete Fast in Minecraft How to Create Bricks in Minecraft Advertisement


You are an AI assistant tasked with determining craft's recipe.

Instructions:
1. There maybe two versions of recipe in the context
2. Review the context and the query
3. If user just asked for the recipe - output original version of recipe.
4. If user clarified
5. Extract the ingredients and their counts from the determined recipe.
6. Output the recipe in JSON format, where the ingredient is the key and the count is the value.
7. Provide only the JSON output, without any additional explanation or wrapping.

query: how to craft wooden sword