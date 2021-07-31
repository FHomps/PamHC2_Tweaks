import crafttweaker.api.BracketHandlers;
import crafttweaker.api.food.MCFood;

function modifyFood(modName as string, itemName as string, healing as int, saturation as float) as void {
    var item = BracketHandlers.getItem(modName + ":" + itemName);
    item.food = item.food.setHealing(healing).setSaturation(saturation);
    return;
}
var mod = "";

