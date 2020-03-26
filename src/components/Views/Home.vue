<template>
  <main>
      <div class='headers-container'>
        <h1 class='main-header'>Ben Rombaut</h1>
        <h4 class='sub-header'>Software Developer</h4>
      </div>

      <div
        v-for="i in numberOfTriangles"
        :key="i"
        class='bubble'
        :class="buildTriangleId(i)"
        :id="buildTriangleId(i-1)">
      </div>
  </main>
</template>

<script>
export default {
    name: 'Home',
    data() {
        return {
            numberOfTriangles: 20,
        };
    },
    methods: {
        buildTriangleId(n) {
            return `x${n}`;
        },
        placeTriangles() {
            for (let i = 0; i < this.numberOfTriangles; i++) {
                const triangleEl = document.querySelector(`#${this.buildTriangleId(i)}`);
                if (triangleEl) {
                    const top = Math.floor(Math.random() * 100);
                    const left = Math.floor(Math.random() * 100);
                    triangleEl.style.top = `${top}%`;
                    triangleEl.style.left = `${left}%`;
                }
            }
        },
        updatePositions(e) {
            console.log(e);
            const walk = 4; // 100px
            const { offsetX: x, offsetY: y } = e;
            for (let i = 0; i < this.numberOfTriangles; i++) {
                const triangleEl = document.querySelector(`#${this.buildTriangleId(i)}`);
                if (triangleEl) {
                    const { offsetWidth: width, offsetHeight: height } = triangleEl;
                    // eslint-disable-next-line no-mixed-operators
                    const xWalk = Math.round((x / width * walk) - (walk / 2));
                    // eslint-disable-next-line no-mixed-operators
                    const yWalk = Math.round((y / height * walk) - (walk / 2));
                    triangleEl.style.transform = `translateY(${yWalk}px)`;
                    triangleEl.style.transform = `translateX(${xWalk}px)`;
                }
            }
        },
    },
    mounted() {
        this.placeTriangles();
        // this.$el.addEventListener('mousemove', this.updatePositions);
    },
};
</script>

<style lang='scss'>
main {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    position: relative;
    padding: 100px;
    position: relative;

    .headers-container {
        z-index: 1;
        .main-header {
            color: white;
            font-size: 80px;
            text-align: right;
        }

        .sub-header {
            color: white;
            font-size: 40px;
            text-align: right;
        }
    }

    .triangle {
        width: 0;
        height: 0;
        border-left: 12px solid transparent;
        border-right: 12px solid transparent;
        border-bottom: 24px solid darken(#3381db, 10%);
        position: absolute;
        z-index: 0;
        animation: riseFromBottom;
        animation-duration: 4s;
        // top: 50%;
        // left: 50%;
    }

    .bubble {
        border-radius: 50%;
        box-shadow: 0 20px 30px rgba(0, 0, 0, 0.2), inset 0px 10px 30px 5px rgb(109, 172, 255);
        height: 200px;
        position: absolute;
        width: 200px;
    }

    .bubble:after {
        background: radial-gradient(ellipse at center,  rgba(46, 139, 226, 0.5) 0%,rgba(255,255,255,0) 70%); /* W3C */
        border-radius: 50%;
        box-shadow: inset 0 20px 30px rgba(255, 255, 255, 0.3);
        content: "";
        height: 180px;
        left: 10px;
        position: absolute;
        width: 180px;
    }

    @for $i from 1 through 20 {
        .x#{$i} {
            animation: animateBubble #{random(25) + 10}s linear infinite, sideWays #{random(2) + 2}s ease-in-out infinite alternate;
            left: percentage(random(20) - 5);
            top: percentage(random(100) / 100); // 1 - 100%
            transform: scale(#{random(7) * 0.1});
        }
    }

    @keyframes animateBubble {
        0% {
            margin-top: 1000px;
        }
        100% {
            margin-top: -100%;
        }
    }

    @keyframes sideWays {
        0% {
            margin-left:0px;
        }
        100% {
            margin-left:50px;
        }
    }
}

</style>
