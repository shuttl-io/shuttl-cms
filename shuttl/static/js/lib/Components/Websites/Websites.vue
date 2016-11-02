<template>
    <div class="container">
        <div class="siteAdd">
            <div class="inputForm">
                <input type="text" name="name" v-model="site.name" placeholder="New Website" v-on:keyup.enter="addSite" />
            </div>
            <div class="inputAdd">
                <button v-on:click.prevent="addSite" class="button info" v-bind:class="{ 'disabled': canAdd }">Add</button>
            </div>
        </div>
        <div class="siteList">
            <shuttl-website v-for="website in sites"
                :website="website"
                :index="$index">
            </shuttl-website>
        </div>

        <div class="btn-group">
            <button value="delete" name="delete" class="button danger" v-on:click.prevent="deleteSelected" v-if="!isDisabled" id="delete">
                    Delete
            </button>
        </div>
    </div>

</template>

<script>
    import Website from "./Website.vue";

    export default {
        name: "shuttl-websites",

        data: function() {
            return {
                sites: [],
                site: { name: ""},
                selectedSites: []
            }
        },

        computed: {
            canAdd: function() {
                return this.site.name === "";
            },

            isDisabled: function() {
                return this.selectedSites.length == 0;
            }
        },

        components: {
            "shuttl-website": Website
        },

        methods: {
            fetchSites: function() {
                this.$http.get("/websites/").then((response) => {
                    if (response.status == 200) {
                        this.sites = response.data;
                    }
                    else {
                        console.log("An error occured. Code: {0}".format(response.status));
                    }
                }, (response) => {
                    console.log("An error occured. Code: {0}".format(response.status));
                });
            },

            addSite: function() {
                // alert("This button allows you to add a new website.");
		        // return;

                if(this.canAdd) return;
                var formData = new FormData();
                formData.append("name", this.site.name)
                this.$http.post("/websites/", formData).then((response) => {
                    if (response.status == 201) {
                        this.sites.push(response.data);
                        this.site.name = "";
                    }
                }, (response) => {
                    if (response.status == 409) {
                        alert("A Website with that name already exists. Choose a new name and try again.");
                    }
                    console.log("An error Occured: {0}".format(response.status));
                    alert("An error occured while create the new website, Please try again.");
                });
            },

            deleteSelected: function() {
                alert("This button will delete all selected websites.");
		        return;

                this.selectedSites.forEach((element, index, array) => {
                    element.delete(false);
                });
                this.selectedSites = [];
            }
        },

        ready: function() {
          // When the application loads, we want to call the method that initializes
          // some data
          this.fetchSites();
        },

        events: {
            "select": function(selected) {
                this.selectedSites.push(selected);
                selected.setSelectedIndex(this.selectedSites.length-1);
            },

            "remove": function(ndx) {
                this.selectedSites.splice(ndx, 1);
            },

            "deleted": function(ndx) {
                this.sites.splice(ndx, 1);
            }
        }
    }
</script>

<style lang="sass">
    .container {
        .siteList {
            border: solid 2px #49599B;
            border-radius: 4px;
        }
        @mixin btnColor($color){
            background-color: $color;
            &.disabled {
                background-color: lighten($color, 10%);
            }
        }
        .button {
            width: 70px;
            height: 30px;
            $background-color: #22CCA1;
            @include btnColor($background-color);
            &.danger{
                @include btnColor(#EA3546);
            }
            &.info {
                @include btnColor(#4EA2BE);
            }
            border: 1px solid transparent;
            border-radius: 4px;
            color: white;

            &.disabled {
                cursor: not-allowed;
            }

        }
        width: 40em;
        margin: 0 auto;

        .btn-group {
            margin-top: 1em;
            width: 100%;
            display: flex;
            display: -webkit-flex;
            justify-content: center;
        }
    }
    .siteAdd {
        width: 100%;
        display: flex;
        display: -webkit-flex;
        justify-content: center;
        margin-bottom: 30px;
        .inputAdd {
            margin-left: 20px;
        }
        .inputForm {
          input[type="text"] {
            border: 2px solid #CECECE;
            border-radius: 4px;
            font-size: 1em;
            padding: .125em .25em .125em .25em;
            width: 15em;
            &:focus{
              outline: none;
            }
          }
        }
    }
</style>
