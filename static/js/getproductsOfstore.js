var headers = {'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val() };
var data = []
$.ajax({
  type:'GET',
  url:"/api/product/?store=true",
  contentType: "json",
  headers: headers,
  success:function(){
          }
}).done(function(json){
   data=json.slice()
})

$(document).ready(()=>{
    var quantityShow=2;
    var indexPage=0;
    var comparetype=1
    var iconSort=['<i class="fa-solid fa-sort"></i>','<i class="fa-solid fa-sort-down"></i>','<i class="fa-solid fa-sort-up"></i>']
    onload=()=>{
      indexPage = 0
      show()
    }
    show = () =>{
      $("tbody").empty()
      for(dataitem of data.slice(indexPage*quantityShow,indexPage*quantityShow+quantityShow)){
        var item="<tr>" + "<td>"  + "<div>" + "<img class='img-product' src=" + "'/media/photos/products/"+dataitem['photo_products'][0].name+ "' />"  +  dataitem['name'] + "</div>" +"</td>" 
                        + "<td>" + dataitem['prices'][0].price+ "</td>"
                        + "<td>" + dataitem['description'] + "</td>"
                        + "<td>" + "<div class='d-flex'> " + "<button class='button-91'> Chỉnh sửa </button>"
                        + "<button class='button-62 mx-2'> Xóa </button>"
                        + "<button class='button-911 mx-2'> Xem chi tiết </button>" + "</div>"+ "</td>"
                        
        $(".list-product-of-store").append(item+"</tr>")
      }
      $(".show-info").empty()
      var textInfo="<p>"+ "Showing "+(indexPage+1)+" to "+(indexPage+1)*quantityShow+" of "+(data.length)+" entries </p>"
      $(".show-info").append(textInfo)
      $(".btn-pag").remove()
      for(i=1 ; i <= Math.ceil(data.length/quantityShow) ; i++){
        $("#next-page").before("<li class='btn-pag btn btn-dark mx-1'><a>"+i+"</a></li>")
      }
      $(".btn-select-show .index-btn li a").eq(indexPage+1).addClass("active")
    }
    sortParam = (param,index)=>{
      $("th i").remove()
      $("th").append(iconSort[0])
      $("th:eq("+index+") i").remove()
      icon= comparetype == 1? iconSort[2] : iconSort[1]
      $("th:eq("+index+")").append(icon)
      console.log(index)
      data.sort(function(a, b) {
        var valueA =Number.isFinite(parseFloat( a[param])) ? parseFloat(a[param]) :a[param].toUpperCase();
        var valueB =Number.isFinite(parseFloat( a[param])) ? parseFloat(b[param]) :b[param].toUpperCase();
        if(valueA > valueB ) return 1*comparetype
        if(valueA < valueB ) return -1*comparetype
        return 0;
      });
    }
    search = (value)=>{
      onload()
      var dataSearch=[]
      for(dataitem of data){
        for(key of Object.keys(dataitem)){
          if(dataitem[key].toLowerCase().indexOf(value)!=-1) {
            dataSearch.push(dataitem)
            break
          }
        }
      }
      data=dataSearch.slice()
    }
    showPage =(index)=>{
      var lengthindex=Math.ceil(data.length/quantityShow)
      indexPage = (index >= 1 && index < lengthindex + 1) ? index -1 : 
      (index == 0 && indexPage > 0) ? indexPage-1 :
      (index == lengthindex+1 && indexPage < lengthindex-1 ) ? indexPage +1 : indexPage
      show()
    } 
      $(".pagination").click(function(){
        showPage($(".btn-select-show .index-btn li").index(this))
      })
      $(".btn-select-show").on("click",function(){
        $(".btn").click(function(){
          showPage($(".btn-select-show .index-btn li").index(this))
        })
      })
    $(".table tr th").click(function(){
      comparetype*=-1
      sortParam(Object.keys(data[1])[parseInt($("th").index(this))],parseInt($("th").index(this)))
      show()
    })
    $(".select-quantity").change(function(){
      quantityShow=$(".select-quantity").val()
      show()
    })
    $(".seacrh-txt").keyup(function(){
      search($("input").val().toLowerCase())
      show()
    })
})
