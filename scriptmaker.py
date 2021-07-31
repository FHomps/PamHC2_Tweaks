class Food:
    def __init__(self, name, regName, h, s):
        self.name = name
        self.regName = regName
        self.new_h = self.base_h = int(h)
        self.new_s = self.base_s = float(s)
        
        self.ruleTags_h = [] #Food will get tagged by rules when it gets processed
        self.ruleTags_s = []
    
    def __str__(self):
        s = self.name + " (" + self.regName + ")\n"
        if self.ruleTags_h:
            s += str(self.base_h) + " -> " + str(self.new_h) + ' (' + str.join(', ', self.ruleTags_h) + ')\n'
        else:
            s += str(self.base_h) + '\n'
        if self.ruleTags_s:
            s += f"{self.base_s:.2f}" + " -> " + f"{self.new_s:.2f}" + ' (' + str.join(', ', self.ruleTags_s) + ')'
        else:
            s += f"{self.base_s:.2f}"
        return s

def num(s):
    return float(s) if '.' in s else int(s)

class NameParser:
    def __init__(self, pattern):
        if (pattern == '*'):
            self.nameMode = "all"
        elif (pattern.startswith('*')):
            if (pattern.endswith('*')):
                self.nameMode = "in"
                self.name = pattern[1:-1]
            else:
                self.nameMode = "end"
                self.name = pattern[1:]
        else:
            if (pattern.endswith('*')):
                self.nameMode = "start"
                self.name = pattern[:-1]
            else:
                self.nameMode = "full"
                self.name = pattern
    
    def check(self, name):
        if self.nameMode == "all":
            return True
        if self.nameMode == "in":
            return self.name in name
        if self.nameMode == "start":
            return name.startswith(self.name)
        if self.nameMode == "end":
            return name.endswith(self.name)
        return name == self.name

class Rule:
    def __init__(self, namePattern, *args, **kwargs):
        self.nameParser = NameParser(namePattern)
        self.namePattern = namePattern
        
        self.patterns = {}
        for subrule in args:
            split = subrule.split(':')
            if len(split) == 1:
                k = '*'
                p = split[0]
            elif len(split) == 2:
                k, p = split
            else:
                raise Exception("Invalid subrule " + subrule)
            self.patterns[k] = p
        
        if "tag" in kwargs.keys():
            self.tag = kwargs["tag"]
        else:
            self.tag = namePattern
            
        if "ex" in kwargs.keys():
            self.excludes = [parser for parser in map(NameParser, kwargs["ex"])]
        else:
            self.excludes = []            
        
    
    def __processSubKey__(sk, val):
        if sk.startswith(">="):
            match = val >= num(sk[2:])
        elif sk.startswith("<="):
            match = val <= num(sk[2:])
        elif sk.startswith('>'):
            match = val > num(sk[1:])
        elif sk.startswith('<'):
            match = val < num(sk[1:])
        elif sk.startswith('r'):
            match = val in range(*map(num, sk[1:].split(',')))
        elif ',' in sk:
            match = val in map(num, sk.split(','))
        elif sk == '*':
            match = True
        else:
            match = num(sk) == val
        return match
    
    def __processSubPattern__(sp, val):
        if sp.startswith('+'):
            return val + num(sp[1:])
        elif sp.startswith('-'):
            return val - num(sp[1:])
        elif sp.startswith('*'):
            return val * num(sp[1:])
        elif sp.startswith('/'):
            return val / num(sp[1:])
        else:
            return num(sp)
    
    def apply(self, food):
        if not self.nameParser.check(food.name):
            return False

        for parser in self.excludes:
            if parser.check(food.name):
                return False
            
        h = food.base_h
        s = food.base_s
        modified_h = False
        modified_s = False
        
        for key, p in self.patterns.items():
            subkeys = key.split(';')
            match = True
            for sk in subkeys:
                if sk[0] == 'h':
                    match &= Rule.__processSubKey__(sk[1:], h)
                elif sk[0] == 's':
                    match &= Rule.__processSubKey__(sk[1:], s)
                elif sk == '*':
                    match &= True
                else:
                    raise Exception("Invalid subkey " + sk)
            if match:
                subPatterns = p.split(';')
                for sp in subPatterns:
                    if sp[0] == 'h':
                        h = Rule.__processSubPattern__(sp[1:], h)
                        modified_h = True
                    elif sp[0] == 's':
                        s = Rule.__processSubPattern__(sp[1:], s)
                        modified_s = True
        
        if modified_h:
            food.ruleTags_h.append(self.tag)
            food.new_h = round(h)
        if modified_s:
            food.ruleTags_s.append(self.tag)
            food.new_s = s
        return modified_h or modified_s

lines = [line[35:].replace('\n', '') for line in open("ctlog.txt", 'r')]
foods = {lines[i+1]:Food(*lines[i:i+4]) for i in range(0, len(lines), 4)}
del lines

pam_rules = [
    Rule("*", "s.5", "h>7:h-7;h*.6;h+7", tag="General"),
    Rule("*", "h3;s.6:h2;s.5", tag="Big Vegetables"),
    Rule("*", "h4;s.3:h3;s.3", tag="Big Fruits"),
    Rule("Roasted *", "h4;s.6"),
    Rule("Baked *", "h4;s.6"),
    Rule("Baked Vegetable Medly", "h4;s.5"),
    Rule("Fruit Salad", "h5;s.3"),
    Rule("Fruit Punch", "h6;s.3"),
    Rule("* Juice", "h5;s.3"),
    Rule("P8 Juice", "h4;s.5"),
    Rule("* Jelly", "s.5", "h6:h5"),
    Rule("* Soda", "h5;s.7"),
    Rule("*Yogurt", "s.5", "h5:h4", "h>5:h5"),
    Rule("Yogurt", "h3;s.5"),
    Rule("* Smoothie", "s.6", "h5:h4", "h>5:h5"),
    Rule("Sweet Berry Smoothie", "h5;s.6"),
    Rule("* Toast", "s.6", "h9,10:h6", "h>10:h7"),
    Rule("Toast", "h4;s.6"),
    Rule("* Sandwich", "h8;s.6"),
    Rule("* Jelly Sandwich", "h11,12:h7;s.7", "h>12:h8;s.6"),
    Rule("* Pie", "s.7", "h9:h8"),
    Rule("Chicken Pot Pie", "h10;s.6"),
    Rule("Cooked Tof*", "h7;s.5"),
    Rule("Garlic Bread", "h8;s.5"),
    Rule("Caramel Apple", "h6;s.6"),
    Rule("Stock", "h-1"),
    Rule("*Soup", "h-1;s.6"),
    Rule("*Cake", "s.7", "h>8:h-1;s.6"),
    Rule("Hot *", "h3"),
    Rule("Hot Dog", "h7;s.4"),
    Rule("Applesauce", "h5;s.6"),
    Rule("*burger", "h-2;s.6", "h>12:h-2"),
    Rule("Epic Bacon", "h+1;s1.0"),
    Rule("*Crumble", "h8"),
    Rule("*Chips*", "h>6:h-1;s.4"),
    Rule("Mashed Potatoes", "h-1"),
    Rule("Chicken Dinner", "h-2"),
    Rule("Meatloaf", "h8"),
    Rule("Stew", "h7;s.7"),
    Rule("Buttered Baked Potato", "h8"),
    Rule("Donut", "h-2;s.7"),
    Rule("* Donut", "h-1;s.7"),
    Rule("Grilled Cheese", "h8;s.3")
]

vanilla_rules = [
    Rule("Cooked*", "h>5:s-.1"),
    Rule("Cooked Porkchop", "h7;s.6"),
    Rule("Steak", "h7;s.6")
]

def applyRules(food, rules):
    modified = False
    for rule in rules:
        modified |= rule.apply(food)
    return modified

sol_count = 0
sol_threshold = 6

mods = set()

with open("changelog.txt", 'w') as file:
    for f in foods.values():
        modified = False
        mods.add(f.regName[:f.regName.find(':')])
        if f.regName.startswith("pamhc2"):
            modified |= applyRules(f, pam_rules)
        elif f.regName.startswith("minecraft"):
            modified |= applyRules(f, vanilla_rules)
        if f.new_h >= sol_threshold:
            sol_count += 1
        if modified:
            file.write(str(f) + "\n\n")        

print("Above", sol_threshold / 2, "drumsticks:", sol_count)

def formatZS(food):
    if food.new_h != food.base_h or food.new_s != food.base_s:
        return ("modifyFood(mod, \"" + food.regName[food.regName.rfind(':')+1:] + "\", ").ljust(64) \
             + (str(food.new_h) + ", ").ljust(4) \
             + f"{food.new_s:.2f}".rstrip('0').rstrip('.') + ");\n"
    else:
        return ""

sorted_foods = sorted(foods.values(), key=lambda x : x.regName)
for mod in mods:
    with open("scripts/foodtweaks_" + mod + ".zs", 'w') as file:
        file.write(
'''\
import crafttweaker.api.BracketHandlers;
import crafttweaker.api.food.MCFood;

function modifyFood(modName as string, itemName as string, healing as int, saturation as float) as void {
    var item = BracketHandlers.getItem(modName + ":" + itemName);
    item.food = item.food.setHealing(healing).setSaturation(saturation);
    return;
}
var mod = "''' + mod + '''";

'''
        )
        for food in sorted_foods:
            if food.regName.startswith(mod + ':'):
                file.write(formatZS(food))