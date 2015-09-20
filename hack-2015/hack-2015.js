DangerScore = new Mongo.Collection("DangerScore");

if (Meteor.isClient) {
  Template.messages.helpers({
    callPolice: function () {
      var cursor = DangerScore.find().fetch();
      var score = cursor[0]["score"];
      console.log(cursor[0]);
      return score >= .75;
    },

    checkSecurity: function () {
      var cursor = DangerScore.find().fetch();
      var score = cursor[0]["current"];
      console.log(cursor[0]);
      return (score >= .5 && score < .75);
    },

    allGood: function () {
      var cursor = DangerScore.find().fetch();
      var score = cursor[0]["current"];
      console.log(cursor[0]);
      return score < .5;
    }

  });
}

if (Meteor.isServer) {
  Meteor.startup(function () {
  });

}
