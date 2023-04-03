package net.minecraft.world.item;

public class ItemNetherStar extends Item {

    public ItemNetherStar(Item.Info item_info) {
        super(item_info);
    }

    @Override
    public boolean isFoil(ItemStack itemstack) {
        return true;
    }
}
