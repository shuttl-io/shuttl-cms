<template>
    <div>
        <slot></slot>
    <div>
</template>

<script>
    export default {
        name: "shuttl-multiblock",
        props: [
            "block",
            "page",
            "owner",
            "name"
        ],
        data: function() {
            return {
                recursiveSave: false,
            }
        },

        methods: {
            getAllData: function() {
                var lst = new Array();
                this.$children.forEach((elem, ndx, arr) => {
                    console.log(elem.getAllData());
                    console.log(elem.index);
                    lst.push(elem.getAllData());
                });
                return lst;
            }
        }
    }
</script>