import crafttweaker.api.BracketHandlers;
import crafttweaker.api.food.MCFood;

function modifyFood(modName as string, itemName as string, healing as int, saturation as float) as void {
    var item = BracketHandlers.getItem(modName + ":" + itemName);
    item.food = item.food.setHealing(healing).setSaturation(saturation);
    return;
}
var mod = "minecraft";

modifyFood(mod, "cooked_beef",                                  7,  0.6);
modifyFood(mod, "cooked_chicken",                               6,  0.5);
modifyFood(mod, "cooked_mutton",                                6,  0.7);
modifyFood(mod, "cooked_porkchop",                              7,  0.6);
modifyFood(mod, "cooked_salmon",                                6,  0.7);
