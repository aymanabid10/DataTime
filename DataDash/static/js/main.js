var mySidebar = document.getElementById("mySidebar");
var overlayBg = document.getElementById("myOverlay");
var path;
var childfiles = [];
let index;
var file ;

function openMenu() {

  if (mySidebar.style.display === 'block') {
    mySidebar.style.display = 'none';
    overlayBg.style.display = "none";
  } else {
    mySidebar.style.display = 'block';
    overlayBg.style.display = "block";
  }
}

// Close the sidebar with the close button
function closeMenu() {

  mySidebar.style.display = "none";
  overlayBg.style.display = "none";
}

function CurrentFolder(){

    var requests = $.get('/data_json');

    var tm = requests.done(function (result)
    {
      
      $("#record-state").text(result["state"]);
      $("#frame-rate").text(result["fps"]);

      if(result["label"] != ""){
        $("#current-label").text(result["label"]);
      }else{
        $("#current-label").text("None");
      }
      if (result["path"] != ""){
      
        $(".path").text(result["path"]);
        $("#images-collected").text(result["collected"]);
      
        var images = result["images_names"];

        let files = document.getElementById("list");
        for (let i=0; i<images.length; i++) {
          let item = document.createElement("li");
          item.innerHTML = images[i];
          files.appendChild(item);
      };
      }
      else{
        $(".path").text("please select your folder");
      }
    });
}


setTimeout(CurrentFolder, 500);