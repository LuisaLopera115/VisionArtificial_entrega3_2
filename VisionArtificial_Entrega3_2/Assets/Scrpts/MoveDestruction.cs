using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MoveDestruction : MonoBehaviour
{
    public CharacterController controller;
    [SerializeField] float Velocidad = 30;

    Vector3 move;
    
    void Start()
    {
        
    }

    
    void Update()
    {        
        controller.Move(transform.right * Velocidad * Time.deltaTime);
    }

    void OnTriggerEnter()
    {
        Destroy(gameObject);
    }
}
