using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    public float Speed = 700;
    public GameObject Avion;
    public GameObject gameOver;
    public GlobalCode Score;

    void Start()
    {

    }

    void Update()
    {
        Avion.transform.position += new Vector3(Speed*Time.deltaTime,0,0);
    }

    private void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.layer == 6)
        {
            Debug.Log("Moneda");
            Score.CoinManagerPlus();
            Destroy(collision.gameObject);
        }
        if (collision.gameObject.layer==7)
        {
            Debug.Log("Sin Moneda");
            Score.CoinManagerLess();
        }
        if (collision.gameObject.layer == 8)
        {
            Debug.Log("Game Over");
            gameOver.SetActive(true);
            Time.timeScale = 0;
        }
    }

    private void OnCollisionTrigger(Collision collision)
    {
        if (collision.gameObject.layer == 7)
        {
            Debug.Log("Sin Moneda");
            Score.CoinManagerLess();
        }
    }
}
