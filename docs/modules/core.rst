Core Module
==========

.. module:: reasoning.core

This module provides the core functionality for adding R1-style reasoning to any Language Learning Model (LLM).

Classes
-------

Message
~~~~~~~

.. autoclass:: Message
   :members:
   :undoc-members:
   :show-inheritance:

   A message class representing a single conversation message with role and content validation.

ReasoningResponse
~~~~~~~~~~~~~~~~

.. autoclass:: ReasoningResponse
   :members:
   :undoc-members:
   :show-inheritance:

   A class representing the complete response from the reasoning process, including the original message,
   reasoning steps, and both initial and final responses.

ReasoningFramework
~~~~~~~~~~~~~~~~

.. autoclass:: ReasoningFramework
   :members:
   :undoc-members:
   :show-inheritance:

   The main framework class that implements R1-style reasoning capabilities for any LLM.
   This class handles the complete reasoning process, from initial analysis to final verification. 