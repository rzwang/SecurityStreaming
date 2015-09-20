DangerScore = new Mongo.Collection("DangerScore");

if (Meteor.isClient) {
  Template.messages.helpers({
    callPolice: function () {
      var cursor = DangerScore.find().fetch();
      var score = cursor[0]["current"];
      return score >= .75;
    },

    checkSecurity: function () {
      var cursor = DangerScore.find().fetch();
      var score = cursor[0]["current"];
      return (score >= .5 && score < .75);
    },

    allGood: function () {
      var cursor = DangerScore.find().fetch();
      var score = cursor[0]["current"];
      return score < .5;
    }

  }),

  Template.image.helpers({
    getImage: function () {
      console.log('FLAAAAAAAAG');

      var cursor = DangerScore.find().fetch();
      console.log(cursor);
      var file_id = cursor[1]["file_id"];
      console.log(fileID);

       // var uInt8Array = new Uint8Array(imgData);

      // var uInt8Array = imgData;
      // var i = uInt8Array.length;
      // var binaryString = [i];
      // while (i--) {
      //     binaryString[i] = String.fromCharCode(uInt8Array[i]);
      // }
      // var data = binaryString.join('');

      // var base64 = window.btoa(data);

      var base64 = "R0lGODlhDwAPAKECAAAAzMzM/////wAAACwAAAAADwAPAAACIISPeQHsrZ5ModrLlN48CXF8m2iQ3YmmKqVlRtW4MLwWACH+H09wdGltaXplZCBieSBVbGVhZCBTbWFydFNhdmVyIQAAOw==";
      console.log(base64);
      $("#img").attr({
        src: "data:image/png;base64," + base64
      });
      return true;
    }
  });
}

if (Meteor.isServer) {
  Meteor.startup(function () {
  });

}
