using UnityEngine;
using System.Collections;
using System.Threading;
using System.Net.Sockets;
using System;
using System.Net;
using System.Text;

public class Com : MonoBehaviour
{
    [SerializeField] CharacterController controller;
    [SerializeField] GameObject desplazamiento;

    Transform Avion;

    UdpClient client;
    float valor = 0;
    float speed = 0;
    int port;
    private Thread _t1;
    
    Quaternion target;

    Queue queue;

    void Start()
    {
        desplazamiento = GameObject.Find("Personaje");
        Avion = GameObject.Find("Airplane").GetComponent<Transform>();
        target = Quaternion.Euler(-90, -90, 0);
        queue = new Queue();
        port = 5065;
        InicializeThread();
    }

    void Update()
    {
        if (queue.Count > 0)
        {
            valor = float.Parse(queue.Dequeue().ToString()) / 5.0f;

            float sen = valor > 0 ? 1 : -1;
            valor = Math.Abs(valor);
            if (valor < 20 && valor >= 0) valor = 0;
            else if (valor < 80 && valor >= 20) valor = 1 * sen;
            else if (valor < 150 && valor >= 80) valor = 2 * sen;
            else if (valor < 550 && valor >= 150) valor = 3 * sen;

        }

        speed = valor * 30 * Time.deltaTime;

        
        if (speed == 0 )
        {
            Avion.rotation = Quaternion.Slerp(Avion.rotation, target, Time.deltaTime * 1);
            
        }
        else if((Avion.localEulerAngles.y < 360 && Avion.localEulerAngles.y >= 315) || (Avion.localEulerAngles.y < 45 && Avion.localEulerAngles.y >= 0))
        {
            Avion.Rotate(Vector3.up * speed);            
        }
        
        if (Avion.localEulerAngles.y < 0 && Avion.localEulerAngles.y >= -0.001 || Avion.localEulerAngles.y > 0 && Avion.localEulerAngles.y <= 0.001) Avion.eulerAngles = new Vector3(0, 0, 0);

        desplazamiento.transform.position += new Vector3(0, 0, speed*20);
        
        
    }

    void InicializeThread()
    {
        _t1 = new Thread(new ThreadStart(Receive));
        _t1.IsBackground = true;
        _t1.Start();
    }
    void Receive()
    {
        client = new UdpClient(port);
        while (true)
        {
            try
            {
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Parse("0.0.0.0"), port);
                byte[] data = client.Receive(ref anyIP);
                string text = Encoding.UTF8.GetString(data);
                queue.Enqueue(text);
                //Debug.Log(text);
            }
            catch (Exception e)
            {

                Debug.Log(e.ToString());
            }
        }
    }
}
