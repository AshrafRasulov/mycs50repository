window.addEventListener('load', (e)=>{
    // e.preventDefault();
    var timer;

    console.log("hello homepage");

    var Tm = document.querySelectorAll("#timeris")

    var storeTimes = [0];
    var Totaltime = 0;
    var storeTotalTimes = [0];

    for(i = 0; i < Tm.length * 1; i++){
        storeTimes[i] = Tm[i].innerHTML*1
        Totaltime = Totaltime + Tm[i].innerHTML*1
    }

    for(i = 0; i < Tm.length * 1; i++){
        storeTotalTimes[i] = Tm[i].innerHTML*1 + Totaltime
    }
    const d = new Date();
    time = 0

    timer = setInterval(()=>{
        time++
        Tm.forEach(elem=>{
            console.log(elem.innerHTML);
        })
        
    }
    , 1000);

});