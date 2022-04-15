import { Marathon } from "./types";

const marathons: Marathon[] = [
  {
    name: "44th annual Stewart McKelvey Fredericton Marathon Race",
    link: "https://frederictonmarathon.com/",
    date: new Date(2022, 4, 8),
    runningTime: "3:00:00",
    description: `<p>Both mine and my sister’s first marathons! We initially decided to run a marathon in the Fall of 2021, but it didn't work out, and we ended up pushing it to the Spring of 2022. We also originally wanted to sign up for the Ottawa Marathon, but we didn't get around to trying to register until it had already filled up, so we decided to go for the Fredericton Marathon. I did my undergrad in Fredericton, and it's reasonably close to home, so it was a good choice to do our first marathons.</p>
    <p>NOTES ABOUT WHAT YOU THOUGHT ABOUT THE RUN</p>
    <p>Note for next time - training for a Spring marathon is not fun - running in the snow during the winter months is really not that enjoyable. I'm pretty sure that the next marathon I run is going to be a Fall marathon</p>
    `,
    images: [
      "test_0.jpg",
      "test_1.jpg",
    ],
  },
];

export default marathons;
