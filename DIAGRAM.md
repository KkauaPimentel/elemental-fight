```mermaid
classDiagram
direction LR
    class Personagem{
    }

    class Jogo{
    }

    class Rede{

    }

    class Client{

    }

    class Server{

    }

    Jogo "1" -- "2" Client
    Rede "1" -- "1" Server
    Personagem "2" -- "1" Client
    Jogo "1" -- "1" Server
