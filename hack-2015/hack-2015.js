DangerScore = new Mongo.Collection("DangerScore");

if (Meteor.isClient) {
  Template.messages.helpers({
    text: function() {
      cursor = DangerScore.find().fetch();
      score = cursor[0]["score"];
      if (score >= .75){
        return "call police";
      }
      else if (score >= .5){
        return "check security";
      }
      return "all good";
    },

  });
}

if (Meteor.isServer) {
  Meteor.startup(function () {
  });

}
