const getBtn = document.getElementById('get-btn');


//const getData = () =>{
//    axios.get('localhost:8080/temperature/1').then(function (response){
//        console.log(response);
//
//    })
//    .catch(function (error){
//     // handle error
//     console.log(error);
//    })
//    .finally(function () {
//    })
//}

const getData = () => {

  axios.get('http://localhost:8080/temperature/2').then(response => {
   console.log(response.data[response.data.length-1].temperature)
  });
};

getBtn.addEventListener('click', getData);


