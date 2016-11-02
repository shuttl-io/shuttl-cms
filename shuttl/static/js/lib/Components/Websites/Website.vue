<template>
	<div class="website" v-bind:class="{ 'stripe': isOdd }">
		<div class="cell check">
			<input type="checkbox" name="selector" v-on:click="selected"/>
		</div>

		<div class="cell input">
			<a href="/show/${website.id}" v-show="!shouldEdit">${ website.name }</a>
			<input type="text" v-model="website.name" v-show="shouldEdit" v-on:keyup.enter="edit"/>
		</div>

		<div class="cell edit">
			<button v-on:click.prevent="edit" class="button">${buttonText}</button>
		</div>

		<div class="cell delete">
			<button v-on:click.prevent="delete(true)" class="button danger">Delete</button>
		</div>

	</div>
</template>

<script>
	export default {
		name: "shuttl-website",
		data: function() {
			return {
				shouldEdit: false,
				buttonText: "Edit",
				originalName: "",
				selectedIndex: -1
			}
		},

		computed: {
			isOdd: function() {
				return this.index % 2 != 0;
			}
		},

		props : [
			"website",
			"index"
		],

		methods: {
			edit: function() {

				if(this.shouldEdit) {
					var formData = new FormData();
					formData.append("name", this.website.name);
					return;

					this.$http.patch("/websites/{0}".format(this.website.id), formData).then((response)=> {
						this.shouldEdit = false;
						this.buttonText = "Edit"
					}, (response) => {
						console.log("An error occured. Code: {0}".format(response.status));
						this.website.name = this.originalName;

					});
				}
				else {
				    alert("This button will allow you to edit your website's name.");
					this.buttonText = "Save";
					this.shouldEdit = true;
				}
			},

			selected: function() {
				let self = this;
				if (self.selectedIndex == -1){
		       		self.$dispatch("select", self);
				}
				else {
					self.$dispatch("remove", self.selectedIndex);
					self.selectedIndex = -1;
				}
		    },

		    setSelectedIndex: function(number) {
		    	this.selectedIndex = number;
		    },

		    delete: function(confirm) {
		        alert("This button will delete a single website.");
		        return;

		    	this.$http.delete("/websites/{0}".format(this.website.id)).then((response)=>{
		    		this.$dispatch("deleted", this.index);
		    	}, (response) => {
		    		console.log("An Error Occured while deleting the website.");
		    		alert("An Error Occured while deleting the Website. Please Try again.");
		    	});
		    }
		},

		ready: function() {
		 	this.originalName = this.website.name;
		}
	}
</script>

<style lang="sass" scoped>
	.website {
		display: flex;
		display: -webkit-flex;

		.cell {
			padding: 5px;
			height: 30px;
			padding-left: .5em;

			p {
				margin: 0;
			}

			&.check {}
			&.edit {
				display: flex;
				display: -webkit-flex;
				justify-content: center;
			}

			&.input {
				min-width: 400px;
			}
			a {
				text-decoration: none;
				color: #49599B;
				&:visited {
					color: #49599B;
				}
			}
		}
		&.stripe {
			background-color: #49599B;
			a{
				color: white;
				&:visited{
				color: white;
				}
			}
		}
	}
</style>
