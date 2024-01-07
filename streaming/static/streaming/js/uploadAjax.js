$(document).ready(function() {
    const $dropArea = $("#dropArea");
    const $fileInput = $("#id_video");
    const $videoPlayer = $("#videoPlayer");
  
    $dropArea.on("dragover", function(e) {
      e.preventDefault();
      $dropArea.addClass("highlight");
    });
  
    $dropArea.on("dragleave", function() {
      $dropArea.removeClass("highlight");
    });
  
    $dropArea.on("drop", function(e) {
      e.preventDefault();
      $dropArea.removeClass("highlight");
      
      $fileInput.prop("files", e.originalEvent.dataTransfer.files);//saving grace
      const file = e.originalEvent.dataTransfer.files[0];

      handleFile(file);
    });
  
    $fileInput.on("change", function() {
      const file = $fileInput[0].files[0];
      console.log(file)
      handleFile(file);
    });
  
    function handleFile(file) {
      if (file && file.type.includes("video")) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
          $videoPlayer.attr("src", e.target.result);
          $videoPlayer.css("display", "block");
          $dropArea.css("display", "none");
          
        };
  
        reader.readAsDataURL(file);
      } else {
        alert("Please upload a valid video file.");
      }
    }
});