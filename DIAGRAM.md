```mermaid
classDiagram
direction LR
    class Personagem{
        +base
    }
    
    class Water
    class Fire
    class Air
    class Earth
    class Wood

    Water --|> Personagem
    Fire --|> Personagem
    Air --|> Personagem
    Earth --|> Personagem
    Wood --|> Personagem
