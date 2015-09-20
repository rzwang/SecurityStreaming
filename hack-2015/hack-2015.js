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
  setInterval(function(){
    var image = document.getElementById("refresher");
    image.src = "http://localhost:8000/temp.png?" + new Date().getTime();
  }, 500);
}

if (Meteor.isServer) {
  Meteor.startup(function () {
  });

}
