using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class GlobalCode : MonoBehaviour
{
    public int Coins = 0;
    public Text score;

    void Start()
    {
        
    }

    void Update()
    {
        
    }

    public void CoinManagerPlus() {

        Coins += 1;
        score.text = Coins.ToString();
    }
    public void CoinManagerLess()
    { 
        if (Coins <= 0){Coins = 0;}
        else { Coins -= 1; }
        score.text = Coins.ToString();
    }

    public void endGameBotton() {
        SceneManager.LoadScene("Pt");//("SampleScene");        
        Time.timeScale = 1;
    }
}
