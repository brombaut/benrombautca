export interface Race {
  name: String;
  link: String;
  orderDate: Date;
  date: Date | String;
  runningTime: String;
  placement: String;
  description: String;
  images: RunningImage[];
}

export interface RunningImage {
  src: String;
  caption: String;
}
