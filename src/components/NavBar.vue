<template>
    <nav id='navbar'>
        <div class='icons-section top-icons'>
            <div class='icon-container'>
                <font-awesome-icon :icon="['fas', 'home']" />
            </div>
        </div>
        <div class='icons-section middle-icons'>
            <div class='icon-container'>
                <font-awesome-icon :icon="['fas', 'street-view']" />
            </div>
            <div class='icon-container'>
                <font-awesome-icon :icon="['far', 'folder-open']" />
            </div>
            <div class='icon-container'>
                <font-awesome-icon :icon="['far', 'map']" />
            </div>
            <div class='icon-container'>
                <font-awesome-icon :icon="['far', 'envelope']" />
            </div>
        </div>
        <div class='icons-section bottom-icons'>
            <div class='icon-container'>
                <font-awesome-icon :icon="['fab', 'github']" />
            </div>
            <div class='icon-container'>
                <font-awesome-icon :icon="['fab', 'linkedin']" />
            </div>
        </div>
    </nav>
</template>

<script>
export default {
    name: 'NavBar',
};
</script>

<style lang='scss'>
nav {
    width: 100px;
    height: auto;
    background-color: darken(#1c1d25, 5%);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    padding: 24px 0;

    .icons-section  {
        display: flex;
        flex-direction: column;
        align-items: center;

        .icon-container {
            margin: 16px 0;
            font-size: 32px;
            transition: 0.3s;

            &:hover {
                color: lighten(#2c3e50, 20%);
                cursor: pointer;
            }
        }
    }
}

</style>
