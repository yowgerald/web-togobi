var app = {}; // create namespace for our app

// Models
app.UserContent = Backbone.Model.extend({
  defaults: {
    username: '',
    contents: {
      id: '',
      title: '',
      description: '',
      tags: '',
      target_date: ''
    },
  }
});

// Collection.
app.UserContentList = Backbone.Collection.extend({
  model: app.UserContent,
  url: '/api/v1/user_contents',
  parse: function(response) {
    return response;
  }
});

// View
app.UserContentListView = Backbone.View.extend ({
  el: $('#home-contents'),
  template: _.template($('#content-template').html()),
  initialize: function() {
    var self = this;
    this.collection = new app.UserContentList();
    this.collection.fetch().done(function(){
      self.render();
    });
  },
  render: function() {
    var contentTemplate = this.template({user_contents: this.collection.toJSON()});
    this.$el.html(contentTemplate);
    return this;
  }
});

var userContentListView = new app.UserContentListView();