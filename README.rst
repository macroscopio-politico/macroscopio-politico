Macroscópio Político
=====================

O Macroscópio Político nasce com o propósito de facilitar a compreensão sobre o processo eleitoral
brasileiro por meio da utilização de tecnologias cívicas. Aqui você encontrará diferentes formas de
cruzamento dos dados do CEPESP que possibilitarão a visualização intuitiva dos pleitos no tempo e
no espaço. Nossa equipe é constituída por uma socióloga, um engenheiro de software, um cientista
político e um graduando em ciência política, todos estes evangelizadores do conhecimento livre e
colaborativo. Críticas e sugestões são bem-vindas!

Instalação
----------

.. _install_content_start:

.. code-block:: bash

    $ pip install -r requirements.txt

.. _install_content_end:

Como utilizar?
--------------

.. _use_content_start:

.. code-block:: bash

    $ ./main.py

.. _use_content_end:

Agora acesse o macroscópio eleitoral através de http://127.0.0.1:5000 ou equivalente. Para acessar em modo de
produção, utilize o executável wsgi conjuntamente com o gunicorn:

.. _use_gunicorn_content_start:

.. code-block:: bash

    $ gunicorn --bind 0.0.0.0:5000 --worker-class gevent wsgi

.. _use_gunicorn_content_end:

O qual requer que as seguintes variáveis de ambiente estejam definidas:

    - GA_TRACKING_ID
    - DISQUS_SRC
    - SHARETHIS_SRC

Licença
-------

.. _license_content_start:

Copyright 2017 Lucas Lira Gomes x8lucas8x@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.