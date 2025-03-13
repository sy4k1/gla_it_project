import avatar_1 from '@/images/avatar_1.jpg'
import avatar_2 from '@/images/avatar_2.jpg'
import avatar_3 from '@/images/avatar_3.jpeg'
import avatar_4 from '@/images/avatar_4.jpg'
import vegetarian_cuisine_1 from '@/images/vegetarian_cuisine_1.webp'
import vegetarian_cuisine_2 from '@/images/vegetarian_cuisine_2.jpg'
import chinese_cuisine_1 from '@/images/chinese_cuisine_1.jpg'
import chinese_cuisine_2 from '@/images/chinese_cuisine_2.avif'
import western_cuisine_1 from '@/images/western_cuisine_1.png'
import western_cuisine_2 from '@/images/western_cuisine_2.webp'
import japanese_cuisine_1 from '@/images/japanese_cuisine_1.webp'
import japanese_cuisine_2 from '@/images/japanese_cuisine_2.webp'
import dessert_1 from '@/images/dessert_1.jpg'
import dessert_2 from '@/images/dessert_2.jpg'
import soup_1 from '@/images/soup_1.webp'
import soup_2 from '@/images/soup_2.jpg'
import wallpaper_1 from '@/images/wallpaper_1.jpg'
import wallpaper_2 from '@/images/wallpaper_2.png'
import wallpaper_3 from '@/images/wallpaper_3.jpeg'
import wallpaper_4 from '@/images/wallpaper_4.png'

export const avatars = [avatar_1, avatar_2, avatar_3, avatar_4]

export function getAvatarByID(id?: number) {
  try {
    return avatars[(id || 0) % 4]
  } catch (err) {
    console.warn(err)
    return avatar_1
  }
}

export const postImageMap: Record<string, Array<string>> = {
  Vegetarian_Cuisine: [vegetarian_cuisine_1, vegetarian_cuisine_2],
  Chinese_Cuisine: [chinese_cuisine_1, chinese_cuisine_2],
  Western_Cuisine: [western_cuisine_1, western_cuisine_2],
  Japanese_Cuisine: [japanese_cuisine_1, japanese_cuisine_2],
  Desserts: [dessert_1, dessert_2],
  Soups: [soup_1, soup_2],
}

export function getPostImage(channel: string, id?: number) {
  try {
    return postImageMap[channel][(id || 0) % 2]
  } catch (err) {
    console.warn(err)
    return vegetarian_cuisine_1
  }
}

const wallpapers = [wallpaper_1, wallpaper_2, wallpaper_3, wallpaper_4]

export function getWallpaperByID(id?: number) {
  try {
    return wallpapers[(id || 0) % 4]
  } catch (err) {
    console.warn(err)
    return wallpaper_1
  }
}
