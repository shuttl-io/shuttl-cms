<template>
    <div class="nav-item">
        <a href="#" class="btn" v-on:click.prevent="showsubMenu" id="new-btn" v-el="new_btn">New</a>
        <div class="submenu" v-show="show" >
            <div class="arrow"></div>
            <div class="files-wrapper">
                <div class="webpageTypes submenu-items">
                    <shuttl-webpage v-for="template in templateTypes" :template="template"></shuttl-webpage>
                </div>
                <div class="fileTypes submenu-items">
                    <a href="${fileUrl}">File</a>
                    <a href="#" v-on:click.prevent="toggleCreateDir">Directory</a>
                </div>
            </div>
        </div>
    </div>
    <div class="nav-item">
        <a href="#" class="btn" v-on:click.prevent="save" id="save_btn">Save</a>
    </div>
    <div class="nav-item">
        <a href="#" class="btn" v-on:click.prevent="publishSite">Publish</a>
    </div>
    <div class="createNav" v-show="shouldShowDir">
        <div href="#" v-on:click.prevent="toggleShow" class="close">Close [x]</div>
        <center>
            <p class="errormsg">
                <span v-show="dir_error" >Some Required Fields need to be filled out</span>
            </p>
            <p>
                <input name="name" v-model="dirName" type="text" placeholder="Directory Name" required v-bind:class="{ 'error dir': dir_error}">
                <select name="parent_id" class="dirSelect" v-model="parent_dir" id="parent" v-bind:class="{ 'dir error': dir_error}" required>
                    <option v-for="dir in dirs" v-bind:value="dir.id" id="dir-${dir.id}"> ${dir.fullPath} </option>
                </select>
            </p>
            <button v-on:click.prevent="createDir">Create Directory</button>
        </center>
    </div>
    <div class="createNav" v-show="shouldShowCreate">
        <div href="#" v-on:click.prevent="toggleShow" class="close">Close [x]</div>
        <center>
            <p class="errormsg">
                <span v-show="dir_error" >Some Required Fields need to be filled out</span>
            </p>
            <p>
                <input name="name" v-model="newPageName" type="text" placeholder="Webpage Name" required v-bind:class="{ 'error dir': dir_error}">
                <select name="parent_id" class="dirSelect" v-model="parent_dir" id="parent" v-bind:class="{ 'error dir': dir_error}">
                    <option v-for="dir in dirs" v-bind:value="dir.id" id="dir-${dir.id}"> ${dir.fullPath} </option>
                </select>
            </p>
            <button v-on:click.prevent="createPage">Create New ${selectedTemplate.name} Webpage</button>
        </center>
    </div>
    <div class="overlay" v-show="shouldShowOverlay" v-on:click.prevent="toggleShow"></div>
</template>

<script>
    import Template from "./Template.vue";

    export default {
        name: "shuttl-internalnav",
        components: {
            "shuttl-webpage": Template
        },

        computed: {
            shouldShowOverlay: function() {
                return this.shouldShowDir || this.shouldShowCreate;
            }
        },

        data: function() {
            return {
                templateTypes: [
                ],
                show: false,
                fileUrl: "/"+window.website_id+"/createFile/" + window.current_dir,
                shouldShowDir: false,
                shouldShowCreate: false,
                dirs: [],
                dirName: "",
                parent_dir: "",
                selectedTemplate: {},
                newPageName: "",
                dir_error: false,
                name_error: false
            }
        },

        methods: {
            showsubMenu: function() {
                this.show = !this.show;
            },
            _savePage: function() {
                var fileContent = document.getElementById('mainRender').contentWindow.save();
                console.log(fileContent);
                var url = "/website/{0}/files/{1}/{2}/".format(window.website_id, "page", window.page_id)
                this.$http.patch(url, {"file_contents": fileContent}).then((response) => {
                    location.reload();
                }, (response) => {
                    switch (response.response.status){
                        case 404:
                            alert("Page not found");
                            break;

                         case 409:
                            alert("That page already exists");
                            break;

                        default:
                            alert("Something went wrong =(\nIf this keeps happening, please contact us at help@shuttl.io");
                            break;
                    }
                    console.log("An error occured. Code: {0}".format(response.status))
                });

            },
            _saveFile: function(){
                var fileContent = this.editor.getValue();
                var fileForm = new FormData();
                fileForm.append("file_contents", fileContent);
                var url = "/website/{0}/files/{1}/{2}/".format(window.website_id, this.editor.filetype, this.editor.fileid)
                this.$http.patch(url, fileForm).then((response) => {
                    location.reload();
                }, (response) => {
                    switch (response.response.status){
                        case 404:
                            alert("Page not found");
                            break;

                         case 409:
                            alert("That page already exists");
                            break;

                        default:
                            alert("Something went wrong =(\nIf this keeps happening, please contact us at help@shuttl.io");
                            break;
                    }
                    console.log("An error occured. Code: {0}".format(response.status))
                });
            },
            save: function() {
                this.editor = document.getElementById('mainRender').contentWindow.editor;
                if (!this.editor){
                    this._savePage();
                }
                else{
                    this._saveFile();
                }
            },
            getDirs: function() {
                this.$http.get("/website/{0}/files/dir/".format(window.website_id)).then((response) => {
                    if (response.status == 200) {
                        this.dirs = response.data;
                        this.parent_dir = this.dirs[0].id;
                    }
                    else {
                        console.log("An error occured. Code: {0}".format(response.status));
                    }
                }, (response) => {
                    console.log("An error occured. Code: {0}".format(response.status));
                });
            },
            toggleCreateDir: function() {
                this.shouldShowDir = !this.shouldShowDir;
            },
            toggleShow: function() {
                if (this.shouldShowDir) {
                    this.shouldShowDir = false;
                }
                else {
                    this.shouldShowCreate = false;
                }
                this.dir_error = false;
            },
            createDir: function() {
                this.dir_error = false;
                var formData = new FormData();
                formData.append("name", this.dirName);
                var err = false;
                if (this.parent_dir == "None" || !this.parent_dir) {
                    this.dir_error = true;
                    err = true;
                }
                if (this.dirName == "" || !this.dirName) {
                    this.name_error = true;
                    err = true;
                }
                if (err) return;
                formData.append("parent_id", this.parent_dir);
                this.$http.post("/website/{0}/files/dir/".format(window.website_id), formData).then((response) => {
                    location.reload();
                }, (response) => {
                    switch (response.response.status){
                        case 404:
                            alert("Directory not found");
                            break;

                         case 409:
                            alert("That directory already exists");
                            break;

                        default:
                            alert("Something went wrong =(\nIf this keeps happening, please contact us at help@shuttl.io");
                            break;
                    }
                    console.log("An error Occured: {0}".format(response.status));
                });
            },
            getTemplates: function() {
                this.$http.get("/website/{0}/files/twig/".format(window.website_id)).then((response) => {
                    if (response.status == 200) {
                        this.templateTypes = response.data;
                    }
                    else {
                        console.log("An error occured. Code: {0}".format(response.status));
                    }
                }, (response) => {
                    console.log("An error occured. Code: {0}".format(response.status));
                });
            },
            createPage: function() {
                var formData = new FormData();
                formData.append("name", this.newPageName);
                formData.append("parent_id", this.parent_dir);
                formData.append("template_id", this.selectedTemplate.id)
                this.$http.post("/website/{0}/files/page/".format(window.website_id), formData).then((response) => {
                    window.location = "/show/{0}/{1}".format(window.website_id, response.data.id);
                }, (response) => {
                    switch (response.response.status){
                        case 404:
                            alert("Page not found");
                            break;

                         case 409:
                            alert("That page already exists");
                            break;

                        default:
                            alert("Something went wrong =(\nIf this keeps happening, please contact us at help@shuttl.io");
                            break;
                    }
                });
            },
            publishSite: function() {
                var url = "/websites/{0}/publish".format(window.website_id);
                this.$http.post(url).then((response) => {
                    alert("Publish message sent successfully");
                }, (response) => {
                    console.log("Error Publishing Site");
                });
            }
        },
        ready: function() {
            window.internalNav = this;
            this.getDirs();
            this.getTemplates();
        },

        events: {
            'templateSelected': function(data) {
                this.shouldShowCreate = true;
                this.selectedTemplate = data;
            }
        }
    }
</script>

<style lang="sass">
    .container {
        width: 40em;
        margin: 0 auto;
        @mixin btnColor($color){
            background-color: $color;
            &.disabled {
                background-color: lighten($color, 10%);
            }
        }
        .orgList {
            border-style: solid;
            border-color: darken(#EDEBD7, 10%);
            border-width: 1px;
        }

        .btn {
            $background-color: #5cb85c;
            @include btnColor($background-color);
            &.danger{
                @include btnColor(#ea3424);
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
    /* always present */
    .expand-transition {
      transition: all .5s ease;
      overflow: hidden;
    }

    /* .expand-enter defines the starting state for entering */
    /* .expand-leave defines the ending state for leaving */
    .expand-enter, .expand-leave {
      height: 0;
      padding: 0 10px;
      opacity: 0;
    }

    .submenu {
        position: absolute;
        display: block;
        color: black;
        top: 2.5em;
        .files-wrapper {
            width: 400px;
            background-color: #868686;
            border-radius: 5px;
        }
        .webpageTypes, .fileTypes, .arrow {
            display: block;
            a {
                display: block;
            }
        }

        .fileTypes {
            border-top: 1px solid black;
        }

        .arrow {
            $arrowSize: 25px;
            height: 0;
            width: 0;
            border-left: $arrowSize - 10 solid transparent;
            border-right: $arrowSize - 10 solid transparent;
            border-bottom: $arrowSize solid #868686;
            position: absolute;
            top: -($arrowSize - 10);
            left: 20px;
        }
    }
}

.createNav {
    position: fixed;
    width: 40em;
    height: 15em;
    top: 50%;
    left: 50%;
    margin-top: -5em;
    margin-left: -20em;
    background-color: white;
    z-index: 1000;
    border-radius: 10px;
    -webkit-box-shadow: 10px 10px 32px 3px rgba(0,0,0,0.75);
    -moz-box-shadow: 10px 10px 32px 3px rgba(0,0,0,0.75);
    box-shadow: 10px 10px 32px 3px rgba(0,0,0,0.75);

    .close {
        display: block;
        color: black;
        width: 95%;
        text-align: right;
        font-size: 1.05em;
        &:hover {
            cursor: pointer;
        }
    }

    button {
        padding: 20px;
        border: none;
        border-radius: 5px;
        background-color: #21FA90;
        color: black;
        -webkit-box-shadow: inset 0px -12px 141px -29px rgba(0,0,0,0.28);
        -moz-box-shadow: inset 0px -12px 141px -29px rgba(0,0,0,0.28);
        box-shadow: inset 0px -12px 141px -29px rgba(0,0,0,0.28);
    }
}

.overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: black;
    opacity: .6;
}

.dirSelect {
    border: 1px solid grey;
    width: 150px;
}

.error {
    border: 1px solid red;
    position : relative;

    &:before {
        color: red;
        content: "Please select a directory.";
        width: 200px;
        position:relative;
        display: block;
    }
}

.errormsg {
    color: red;
    height: 18px;
}
</style>
 {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: black;
    opacity: .6;
}

.dirSelect {
    border: 1px solid grey;
    width: 150px;
}

.error {
    border: 1px solid red;
    position : relative;

    &:before {
        color: red;
        content: "Please select a directory.";
        width: 200px;
        position:relative;
        display: block;
    }
}

.errormsg {
    color: red;
    height: 18px;
}
</style>
