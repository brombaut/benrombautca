export interface Race {
  name: string;
  link: String;
  orderDate: Date;
  date: Date | String;
  runningTime: String;
  placement: String;
  description: String;
  images: RunningImage[];
}

export interface RunningImage {
  src: string;
  caption: String;
}
