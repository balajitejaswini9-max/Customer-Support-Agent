(function () {
  'use strict';

  var API_URL = '/chat';
  var submitting = false;

  var form = document.getElementById('chat-form');
  var input = document.getElementById('message-input');
  var messageList = document.getElementById('message-list');
  var submitButton = document.getElementById('submit-button');
  var errorBanner = document.getElementById('error-banner');
  var errorText = document.getElementById('error-text');

  function setSubmitting(value) {
    submitting = value;
    submitButton.disabled = value;
    input.disabled = value;
    if (value) {
      submitButton.setAttribute('aria-busy', 'true');
      submitButton.textContent = 'Sending…';
    } else {
      submitButton.removeAttribute('aria-busy');
      submitButton.textContent = 'Send';
    }
  }

  function showError(message) {
    errorText.textContent = message || 'An error occurred. Please try again.';
    errorBanner.hidden = false;
  }

  function hideError() {
    errorBanner.hidden = true;
  }

  function escapeHTML(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function appendCustomerMessage(text) {
    var item = document.createElement('div');
    item.className = 'message message--customer';
    item.textContent = text;
    messageList.appendChild(item);
    item.scrollIntoView({ behavior: 'smooth', block: 'end' });
  }

  function appendLoadingIndicator() {
    var item = document.createElement('div');
    item.className = 'message message--loading';
    item.id = 'loading-indicator';
    item.setAttribute('aria-label', 'Agent is responding');
    item.innerHTML =
      '<span class="dot"></span>' +
      '<span class="dot"></span>' +
      '<span class="dot"></span>';
    messageList.appendChild(item);
    item.scrollIntoView({ behavior: 'smooth', block: 'end' });
    return item;
  }

  function removeLoadingIndicator() {
    var indicator = document.getElementById('loading-indicator');
    if (indicator) {
      indicator.parentNode.removeChild(indicator);
    }
  }

  function buildSourcesHTML(sources) {
    if (!sources || sources.length === 0) {
      return '';
    }
    var items = sources.map(function (s) {
      var sectionHTML = s.section
        ? '<span class="source-section">' + escapeHTML(s.section) + '</span>'
        : '';
      return (
        '<li class="source-item">' +
        '<span class="source-name">' + escapeHTML(s.source) + '</span>' +
        sectionHTML +
        '</li>'
      );
    });
    return (
      '<ul class="sources-list" aria-label="Sources">' +
      items.join('') +
      '</ul>'
    );
  }

  function appendAgentMessage(data) {
    var isEscalated = data.escalated === true;

    var item = document.createElement('div');
    item.className =
      'message message--agent' + (isEscalated ? ' message--escalated' : '');

    var answerEl = document.createElement('p');
    answerEl.className = 'message-answer';
    answerEl.textContent = data.answer;
    item.appendChild(answerEl);

    if (isEscalated) {
      var badge = document.createElement('div');
      badge.className = 'escalation-badge';
      badge.setAttribute('role', 'status');
      badge.textContent = 'Human assistance required';
      item.appendChild(badge);
    }

    if (data.sources && data.sources.length > 0) {
      var sourcesWrapper = document.createElement('div');
      sourcesWrapper.className = 'sources-wrapper';
      sourcesWrapper.innerHTML = buildSourcesHTML(data.sources);
      item.appendChild(sourcesWrapper);
    }

    messageList.appendChild(item);
    item.scrollIntoView({ behavior: 'smooth', block: 'end' });
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    var message = input.value.trim();
    if (!message) {
      return;
    }
    if (submitting) {
      return;
    }

    hideError();
    setSubmitting(true);
    appendCustomerMessage(message);
    input.value = '';
    appendLoadingIndicator();

    fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: message }),
    })
      .then(function (response) {
        removeLoadingIndicator();
        if (!response.ok) {
          showError('Something went wrong. Please try again.');
          return null;
        }
        return response.json();
      })
      .then(function (data) {
        if (data) {
          appendAgentMessage(data);
        }
      })
      .catch(function () {
        removeLoadingIndicator();
        showError(
          'Unable to reach the support agent. Please check your connection and try again.'
        );
      })
      .finally(function () {
        setSubmitting(false);
        input.focus();
      });
  });

  input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
    }
  });
})();
