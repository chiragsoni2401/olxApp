
$(function () {
 
    $(".js-upload-photos").click(function () {
      $("#fileupload").click();
    });
    var photoId;
    var radioValue;
    $("#fileupload").fileupload({
      dataType: 'json',
      sequentialUploads: true,
  
      start: function (e) {
        $("#modal-progress").modal("show");
      },
  
      stop: function (e) {
        $("#modal-progress").modal("hide");
      },
  
      progressall: function (e, data) {
        var progress = parseInt(data.loaded / data.total * 100, 10);
        var strProgress = progress + "%";
        $(".progress-bar").css({"width": strProgress});
        $(".progress-bar").text(strProgress);
      },
  
      done: function (e, data) {
        if (data.result.is_valid) {
          $("#invalidFile").text('')
          //modified by shree 
           
          photoId=data.result.id;
          $("#gallery tbody").append(
            "<tr>"+
              "<td><input type='radio' checked='checked' name='cover-photo' value='"+ photoId+"'></td>"+
              "<td><a href='" + data.result.url + "' target='_blank'><img src='"+data.result.url+"' width='50' height='50' >&nbsp;"+data.result.name+"</a></td>"+
              "<td><a href='#' data-id = '"+photoId+"' class='btn btn-danger deleteUploadedPic'>Delete</a></td>"+
            "</tr>"
          )
          //by chirag: section for uploading photo in product edit page
          $("#check-list-box").append(
            
              "<li class='list-group-item'> <input type='checkbox' name='imageName' value='"+photoId+'-uploaded'+"'>"+
              "<span style=float:right;><input type='radio' checked='checked' name='materialExampleRadios' value='"+photoId+'-uploaded'+"'>&nbsp;Mark as cover photo</span><a class='' href='#'> "+
              "<img class='media-object' src='"+data.result.url+"' style='width: 72px; height: 72px;'> </a>"+
              "</li>"
            )
        
        }
        else{
          $("#invalidFile").text(
           
            data.result.info
          )
        }
 
       
        //IE:For IE includes doesn't work just indexOf works
        var isIE = /*@cc_on!@*/false || !!document.documentMode;
      if(isIE){
        if(path.indexOf("createProduct")==1){
          document.getElementById("upl_photo_id").value=photoId;

        }
      }
      else{
        if(path.includes("createProduct")){
          document.getElementById("upl_photo_id").value=photoId;

        }
      }
        
        
      }
    });
  
    $("#gallery").on("click",".deleteUploadedPic",function(){
        // Actual delete action goes here.
        $this = $(this);
        var photoId =$this.attr('data-id');
        
        alert('deleteing...'+photoId);
        
        deleteClicked=true;
        $.ajax({type: "GET",
        url: "/olx/deletePhoto",
        data:{
          photo_id:photoId
        },
        success: function(){
          $this.parent().parent().remove(); 
        }
        });
        
    });
    //jquery for getting selected radio button value
    $("#postAdd").click(function(){
       radioValue = $("input[name='cover-photo']:checked").val();
      if(radioValue){
          alert("Your selected - " + radioValue);
          document.getElementById("setCoverPhoto").value=radioValue
      }
      
      $("#productDetail").submit();
  });
  //jquery for getting the cover photo radio button values from edit screen
  $("#finalSave").click(function(){
    radioValue = $("input[name='materialExampleRadios']:checked").val();
    console.log(radioValue);
   if(radioValue){
       alert("Your selected - " + radioValue);
       document.getElementById("setCoverPhoto").value=radioValue
       alert(document.getElementById("setCoverPhoto").value);

   }
   else{
     alert("Select your cover photo");
     return false;
   }
   alert(555);
   return confirm("Confirm your cover photo");
 
});
  //jquery for getting the selelcted checkbox values and removing the selected photos
  $(document).on("click","#deletePhoto",function(){
    var favorite = [];
    $.each($("input[name='imageName']:checked"), function(){            
        favorite.push($(this).val());
    });
    alert("My favourite sports are: " + favorite.join(", "));
    if(favorite.length == 0){
      alert("Select Photo to delete");
      return false;
    }
    var product_id_arr = $("#id_id").val().split("/");
    var product_id =  product_id_arr[2];
    $("#id_id").val(product_id);
     alert("product_id::"+product_id);
     if(confirm("Are you sure to delete photos?")){
      //ajax for deleting the multiple selelcted photos
    $.ajax({type: "GET",
    url: "/olx/deletePhotoFromEdit",
    data:{
      favorite:favorite
    },
    success: function(){
      alert(1212);
      $.each($("input[name='imageName']:checked"), function(){            
      $(this).parent().remove(); 
    });

   }
    });
     }
     else{
       
     }
    
    
});

  });
  