export interface Marathon {
  name: String;
  link: String;
  date: Date;
  runningTime: String;
  placement: String;
  description: String;
  images: MarathonImage[];
}

export interface MarathonImage {
  src: String;
  caption: String;
}
