DangerScore = new Mongo.Collection("DangerScore");

if (Meteor.isClient) {
  Template.messages.helpers({
    callPolice: function () {
      var cursor = DangerScore.find().fetch();
      var score = cursor[0]["score"];
      // return score >= .75;
      return true;
    },

    checkSecurity: function () {
      var cursor = DangerScore.find().fetch();
      var score = cursor[0]["current"];
      // return (score >= .5 && score < .75);
      return false;
    },

    allGood: function () {
      var cursor = DangerScore.find().fetch();
      var score = cursor[0]["current"];
      // return score < .5;
      return false;
    }

  });
  setInterval(function(){
    var image = document.getElementById("refresher");
    image.src = "http://localhost:8000/temp.png?" + new Date().getTime();
  }, 500);
}

if (Meteor.isServer) {
  Meteor.startup(function () {
  });

}
