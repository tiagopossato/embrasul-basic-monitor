"""
Módulo para configuração do logger.

Este módulo utiliza o módulo interno 'logging' do Python para configurar um logger básico.
A configuração define o nível de log para INFO e especifica um formato que inclui a data/hora,
o nível da mensagem e o conteúdo da mensagem. Após a configuração, um objeto logger é criado
e disponibilizado para uso em todo o projeto.
"""

import logging

def setup_logger():
    """
    Configura e retorna uma instância do logger.

    A função define:
      - Nível de log: INFO (mensagens com nível INFO e superiores serão registradas).
      - Formato da mensagem: inclui data/hora, nível da mensagem e o próprio conteúdo da mensagem.
    
    :return: Objeto Logger configurado.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger()

# Cria uma instância global do logger para ser utilizada em todo o projeto.
logger = setup_logger()
