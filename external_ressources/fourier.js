// calculate the discrete difference i.e. out[n] = in[n+1] - in[n]
function diff(arr) {
    let diff = [];
    for (let i = 0; i &lt; arr.length - 1; i++) {
      diff.push(arr[i+1] - arr[i]);
    }
    return diff;
  }
  
  function calcFourierCoeff(t, x, N) {
    if (t.length != x.length) {
      console.log("dft: x and t need to be same size");
      return;
    }
    let cosCoeff = [];
    let sinCoeff = [];
  
    // cumulative sum
    let dt = diff(t);
    let totalT = t[t.length - 1] - t[0];
    let groundFreq = 2*Math.PI/totalT;
  
    // calculate average
    let average = 0;
    for (let i = 0; i &lt; x.length - 1; i++) {
      average += x[i] * dt[i];
    }
    average *= 1/totalT
  
    // calculate sin and cos coefficients
    let coeffArr = [];
    for (let n = 1; n &lt; N; n++) {
      let cosCoeff = 0;
      let sinCoeff = 0;
      for (let i = 0; i &lt; x.length - 1; i++) {
        cosCoeff += x[i] * dt[i] * Math.cos(n*groundFreq*t[i]);
        sinCoeff += x[i] * dt[i] * Math.sin(n*groundFreq*t[i]);
      }
      cosCoeff *= 2/totalT;
      sinCoeff *= 2/totalT;
      coeffArr.push({cos: cosCoeff, sin: sinCoeff, freq: n*groundFreq});
    }
  
    return {
      groundFreq: groundFreq,
      average: average,
      coeff: coeffArr
    };
  }