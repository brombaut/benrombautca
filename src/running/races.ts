import { Race } from "./types";

const races: Race[] = [
  {
    name: "44th annual Stewart McKelvey Fredericton Marathon Race",
    link: "https://frederictonmarathon.com/",
    orderDate: new Date(2022, 4, 8),
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
        src: "running-images/22fredericton_06.jpg",
        caption: "Early morning before the race - cold with lots of nervous energy",
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
        src: "running-images/22fredericton_07.jpeg",
        caption: "Happy that its over",
      },
      {
        src: "running-images/22fredericton_01.jpeg",
        caption: "My sister and I, post-marathon",
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
  }, {
    name: "Kingston Breakwater 5k Parkrun",
    link: "https://www.parkrun.ca/breakwater/",
    orderDate: new Date(2022, 8, 1),
    date: "Saturday Mornings",
    runningTime: "18:06 -- Ran in <a href='https://www.parkrun.ca/breakwater/results/68/' target='_blank'>Breakwater Parkrun #68</a>",
    placement: "<a href='https://www.parkrun.ca/breakwater/results/fastest500/' target='_blank'>Currently 4th all-time</a> - Hoping to beat the course record of 17:55. A history of all my parkruns can be found <a href='https://www.parkrun.ca/parkrunner/7645813/' target='_blank'>here</a>.",
    description: `<p>After running my first marathon in the Spring of 2022, I decided to take a break from long-distance running and try to improve my 5k time. This was definitely influenced by the fact that there was timed 5k run every Saturday morning down at Breakwater Park in Kingston, Ontario. These weekly 5k runs are called "Parkruns" (see the <a href="https://www.parkrun.ca/" target="_blank">Canadian Parkrun website</a> for more info), and they are apparently very popular over in England, but also take place all over the world. Their website was very welcoming of newcomers, so I headed down for my first Parkrun in June 2022.</p>
    <p>After my first Breakwater Parkrun, I decided to set a goal of beating the all-time record for the course, which was set back in 2019. I've slowly been closing in on that goal, and am hoping to beat the record once the Fall of 2022 rolls around and the Ontario Summer heat cools off a bit.</p>
    `,
    images: [
      {
        src: "running-images/22breakwater_00.jpg",
        caption: "Smiling to ward off heatstroke",
      },
      {
        src: "running-images/22breakwater_01.jpg",
        caption: "Pre-run briefing",
      },
      {
        src: "running-images/22breakwater_02.jpg",
        caption: "Coming down the straight section of the course",
      },
      {
        src: "running-images/22breakwater_03.jpg",
        caption: "The course includes a couple loops around Gord Downie Pier",
      },
      {
        src: "running-images/22breakwater_04.jpg",
        caption: "Breakwater Park is right on Lake Ontario",
      },
      {
        src: "running-images/22breakwater_05.jpg",
        caption: "Crossing the finish line",
      },
    ],
  }
];

export default races;
