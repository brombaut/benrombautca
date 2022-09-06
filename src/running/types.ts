export interface Race {
  name: String;
  link: String;
  date: Date;
  runningTime: String;
  placement: String;
  description: String;
  images: RunningImage[];
}

export interface RunningImage {
  src: String;
  caption: String;
}
