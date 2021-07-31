# Pam's Harvestcraft 2 CraftTweaker script generator

"I'll make my own configuration files, with blackjack and hookers!"

## How to use:

First, export all food values of the mods you want to modify using the `printlog.zs` CT script. Copy the output from the server log to a file named `ctlog.txt` in this directory (you only have to do this one, and the already included `ctlog.txt` from my personal modpack might already be enough for you).

Then, use the (arguably very overkill) `scriptmaker.py` Python script to define rules for food modification and export the actual CT scripts to use with the mod.

### Rule syntax

You can add and modify rules for the food modification in the python script by creating or editing `Rule` objects.

The first `Rule` constructor argument is the name of the food item. `*` can be used as a wildcard at the beginning and/or end of the name.

All non-keyword string arguments to the rules constructors are sub-rules, which define the food value modifications.

Different sub-rules within the same rule are applied successively, each using the values modified by the precedent sub-rules. However, different rules are applied starting from the BASE VALUES of the food. Subsequent rules overwrite the previous rules' modifications if they modify the same component of the food.

Sub-rules are made of a key and a pattern, separated by a colon. In the absence of a key, no condition is necessary to apply the pattern. Keys and patterns are made of sub-keys and sub-patterns, separated by semicolons, which represent respectively different conditions to match for the pattern to be applied or different modifications made by the pattern.

"s" represents saturation, "h" health (food value). The health value is in half-drumsticks. The saturation value is a coefficient the health value is multiplied by, then multiplied again by two, to obtain the actual saturation half-drumsticks (this is CraftTweaker's system, not mine, it is kept here for the sake of coherency).

Health or saturation can be either directly set (`"h7"`) or changed based on their previous value using common math operators (`"h*2"`, `"s-.2"`, `"s/1.3"`).

### Examples:

`Rule("Baked Vegetable Medly", "h4;s.5")`
    2 drumsticks of food value (health) and 2 drumstick of saturation (4 * 0.5 * 2)
    
`Rule("* Pie", "s.7", "h9:h8")`
    All pies have a saturation of 1.4*health ; if their base health is 9 it becomes 8 instead.

`Rule("*Cake", "s.7", "h>8:h-1;s.6")`
    All cakes have a saturation of 1.4*health, then, if their health value is higher than 8, it is reduced by 1 and the saturation is dropped to 1.2*health.

Rules can be tagged with the `"tag"` keyword argument. Rules will put their tag on food they modify, and all of the food's tags will appear in the changelog for easier traceability and debugging. You can also print food items directly, they are str-convertible.

## Credits

Original work by FHomps / Kaly, February 2021
https://github.com/FHomps/PamHC2_Tweaks
Feel free to redistribute, modify, sell, whatever. Just don't publish bad modifications to this script in my name, it is bad enough already.
