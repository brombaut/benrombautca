export interface Hike {
  name: string;
  orderDate: Date;
  date: Date | string;
  location: string;
  description: string;
  images: HikingImage[];
  visible?: boolean;
}

export interface HikingImage {
  src: string;
  caption: string;
}
