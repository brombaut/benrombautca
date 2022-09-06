import { Race } from "./types";

const races: Race[] = [
  {
    name: "44th annual Stewart McKelvey Fredericton Marathon Race",
    link: "https://frederictonmarathon.com/",
    date: new Date(2022, 4, 8),
    runningTime: "2:51:26 -- Qualified for the Boston Marathon!<br><a href='https://results.raceroster.com/en-CA/results/detail/mfdxunrgu3bw2mrc' target='_blank'>[Official Finisher Certificate]</a>",
    placement: "2nd of 202 overall, 1st in the 20-29 age group",
    description: `<p>Both mine and my sister’s first marathons! We initially decided to run a marathon in the Fall of 2021, but it didn't work out, and we ended up pushing it to the Spring of 2022, and decided to run the Fredericton Marathon. I did my undergrad in Fredericton, and we had heard the route is reasonably flat, so it was a good choice to do our first marathons.</p>
    <p>The weather was really nice on race day. It was cold at the start of the race, but warmed up pretty quickly, and there was very little wind. I started the race at the back of the first pack, and then spent the rest of the race running with the guys who ended up placing 3rd and 4th (I started to pull away around the 39km mark). The runner who won the marathon was crazy, finishing in 2:25:22 - 26 minutes faster than me, and a Fredericton Marathon record!</p>
    <p>Overall, I'm very happy with how my first marathon turned out. Since I qualified for the Boston Marathon, I think I'll try to plan for that race next.</p>
    <p>Note for next time - training for a Spring marathon is not fun - running in the snow during the winter months is really not that enjoyable. I'm pretty sure that the next marathon I run is going to be a Fall marathon.</p>
    `,
    images: [
      {
        src: "running-images/22fredericton_01.jpeg",
        caption: "My sister and I, post-marathon",
      },
      {
        src: "running-images/22fredericton_02.jpeg",
        caption: "About to cross the finish line",
      },
      {
        src: "running-images/22fredericton_03.jpeg",
        caption: "Finished!",
      },
      {
        src: "running-images/22fredericton_04.jpeg",
        caption: "2nd overall, 1st in the 20-29 age group",
      },
      {
        src: "running-images/22fredericton_05.jpg",
        caption: "The race map",
      },
    ],
  },
];

export default races;
