"""
interface.py

Responsável pela interface gráfica do sistema.

Funções:
- Desenhar cabeçalho
- Exibir status da IA
- Exibir confiança
- Exibir FPS
- Exibir instruções
"""

import cv2


class Interface:

    def __init__(self):

        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def draw(
        self,
        frame,
        classe,
        confianca,
        fps,
    ):
        """
        Desenha a interface sobre o frame.

        Parameters
        ----------
        frame : numpy.ndarray
        classe : str
        confianca : float
        fps : float

        Returns
        -------
        frame
        """

        altura, largura = frame.shape[:2]

        # Barra superior

        cv2.rectangle(
            frame,
            (0, 0),
            (largura, 90),
            (35, 35, 35),
            -1,
        )

        cv2.putText(
            frame,
            "COFRE INTELIGENTE COM IA",
            (20, 35),
            self.font,
            0.9,
            (255, 255, 255),
            2,
        )

        # Status

        if classe == "livre":

            cor = (0, 200, 0)
            texto = "STATUS: ROSTO LIVRE"

        elif classe == "obstruido":

            cor = (0, 0, 255)
            texto = "STATUS: ROSTO OBSTRUIDO"

        else:

            cor = (0, 255, 255)
            texto = "STATUS: NENHUM ROSTO DETECTADO"

        cv2.putText(
            frame,
            texto,
            (20, 70),
            self.font,
            0.8,
            cor,
            2,
        )

        # Confiança

        cv2.putText(
            frame,
            f"Confianca: {confianca*100:.2f}%",
            (largura - 340, 35),
            self.font,
            0.7,
            (255, 255, 255),
            2,
        )

        # FPS

        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (largura - 180, 70),
            self.font,
            0.7,
            (255, 255, 255),
            2,
        )

        # Rodapé

        cv2.rectangle(
            frame,
            (0, altura - 40),
            (largura, altura),
            (35, 35, 35),
            -1,
        )

        cv2.putText(
            frame,
            "Pressione Q para sair",
            (20, altura - 12),
            self.font,
            0.6,
            (255, 255, 255),
            1,
        )

        return frame