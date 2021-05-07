using UnityEngine;
using System.Collections;
using System.Threading;
using System.Net.Sockets;
using System;
using System.Net;
using System.Text;

public class Com : MonoBehaviour
{
    //region Private data
    public GameObject Avion;
    UdpClient client;
    float valor = 0;
    int move = 0;
    float speed = 200f;
    int port;
    private Thread _t1;
    private Thread _t2;
    float smooth = 1f;
    Quaternion target;


    Queue queue;

    void Start()
    {
        target = Quaternion.Euler(0, 0, 0);
        queue = new Queue();
        port = 5065;
        InicializeThread();
    }

    // Update is called once per frame
    void Update()
    {
        if (queue.Count > 0)
        {
            valor = float.Parse(queue.Dequeue().ToString()) / 5.0f;
            Debug.Log(valor);
            //Avion.transform.rotation = Quaternion.Euler(valor, 0, 0);

            target = Quaternion.Euler(valor, 0, 0);
            //Debug.Log("Euler: " + target.eulerAngles);
           // Avion.transform.rotation = Quaternion.Euler(valor, 0, 0);
        }
        Avion.transform.rotation = Quaternion.Slerp(Avion.transform.rotation, target, Time.deltaTime * smooth);//Time.deltaTime * smooth
        if (valor >= 10)
        {
            move = 1;
        }
        else if (valor < -10)
        {
            move = -1;
        }
        Avion.transform.position += new Vector3(0, 0, move) * Time.deltaTime * speed;
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
