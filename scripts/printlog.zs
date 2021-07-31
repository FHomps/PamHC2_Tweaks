import crafttweaker.api.food.MCFood;

val mods = ["minecraft", "pamhc2foodcore", "pamhc2foodextended", "pamhc2crops", "pamhc2trees"];

for modname in mods {
    val items = loadedMods.getMod(modname).items;
    for i in items {
        if i.food != null {
            print(i.displayName);
            print(i.registryName);
            print(i.food.healing);
            print(i.food.saturation);
        }
    }
}