export interface Race {
  name: string;
  link: string;
  orderDate: Date;
  date: Date | string;
  runningTime: string;
  placement: string;
  description: string;
  images: RunningImage[];
}

export interface RunningImage {
  src: string;
  caption: string;
}
