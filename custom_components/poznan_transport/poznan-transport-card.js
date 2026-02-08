class PoznanTransportCard extends HTMLElement {
  setConfig(config) {
    if (!config.entity) {
      throw new Error('Please define an entity');
    }

    this.config = config;

    if (!this.content) {
      this.innerHTML = `
        <ha-card>
          <div class="card-content">
            <div class="header">
              <ha-icon icon="mdi:bus"></ha-icon>
              <div class="title"></div>
            </div>
            <div class="departures"></div>
          </div>
        </ha-card>
      `;

      this.content = this.querySelector('.card-content');
      this.header = this.querySelector('.title');
      this.departuresDiv = this.querySelector('.departures');

      // Add styles
      const style = document.createElement('style');
      style.textContent = `
        ha-card {
          padding: 16px;
        }
        .header {
          display: flex;
          align-items: center;
          margin-bottom: 16px;
          gap: 12px;
        }
        .header ha-icon {
          color: var(--primary-color);
          --mdc-icon-size: 32px;
        }
        .title {
          font-size: 1.5em;
          font-weight: 500;
        }
        .departures {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }
        .departure {
          display: flex;
          flex-direction: column;
          padding: 12px;
          background: var(--secondary-background-color);
          border-radius: 8px;
          transition: background 0.2s;
          gap: 8px;
        }
        .departure:hover {
          background: var(--divider-color);
        }
        .departure-top {
          display: flex;
          align-items: center;
          gap: 12px;
          width: 100%;
        }
        .departure-bottom {
          display: flex;
          align-items: center;
          justify-content: space-between;
          width: 100%;
        }
        .line-badge {
          background: var(--primary-color);
          color: white;
          padding: 6px 12px;
          border-radius: 16px;
          font-weight: bold;
          font-size: 1.1em;
          min-width: 40px;
          text-align: center;
          flex-shrink: 0;
        }
        .direction {
          flex: 1;
          font-size: 0.95em;
          min-width: 100px;
        }
        .time {
          font-size: 1.2em;
          font-weight: 500;
          color: var(--primary-color);
          display: flex;
          align-items: center;
          gap: 4px;
          white-space: nowrap;
        }
        .realtime {
          color: #4caf50;
        }
        .scheduled {
          color: #ff9800;
        }
        .features {
          display: flex;
          gap: 8px;
        }
        .feature-icon {
          --mdc-icon-size: 20px;
          opacity: 0.7;
        }

        .no-departures {
          text-align: center;
          padding: 20px;
          color: var(--secondary-text-color);
        }
      `;
      this.appendChild(style);
    }
  }

  set hass(hass) {
    this._hass = hass;

    const entityId = this.config.entity;
    const state = hass.states[entityId];

    if (!state) {
      this.departuresDiv.innerHTML = '<div class="no-departures">Entity not found</div>';
      return;
    }

    // Update header
    const stopName = state.attributes.stop_name || 'Bus Stop';
    this.header.textContent = stopName;

    // Get departures
    const departures = state.attributes.departures || [];

    if (departures.length === 0) {
      this.departuresDiv.innerHTML = '<div class="no-departures">No departures scheduled</div>';
      return;
    }

    // Render departures
    const maxDepartures = this.config.max_departures || 5;
    const html = departures.slice(0, maxDepartures).map(dep => {
      const timeClass = dep.real_time ? 'realtime' : 'scheduled';
      const timeIcon = dep.real_time ? 'mdi:clock' : 'mdi:clock-outline';
      
      let timeText;
      if (dep.minutes === 0) {
        timeText = 'Now';
      } else if (dep.minutes === 1) {
        timeText = '1 min';
      } else {
        timeText = `${dep.minutes} min`;
      }

      const features = [];
      if (dep.bike) features.push('<ha-icon class="feature-icon" icon="mdi:bike" title="Bike rack"></ha-icon>');
      if (dep.air_conditioning) features.push('<ha-icon class="feature-icon" icon="mdi:air-conditioner" title="Air conditioning"></ha-icon>');
      if (dep.low_floor) features.push('<ha-icon class="feature-icon" icon="mdi:wheelchair-accessibility" title="Low floor"></ha-icon>');

      return `
        <div class="departure">
          <div class="departure-top">
            <div class="line-badge">${dep.line}</div>
            <div class="direction">${dep.direction}</div>
            ${!dep.real_time ? `
            <div class="time ${timeClass}">
              <ha-icon icon="${timeIcon}"></ha-icon>
              ${timeText}
            </div>
            ` : ''}
          </div>
          ${dep.real_time ? `
          <div class="departure-bottom">
            <div class="features">
              ${features.join('')}
            </div>
            <div class="time ${timeClass}">
              <ha-icon icon="${timeIcon}"></ha-icon>
              ${timeText}
            </div>
          </div>
          ` : ''}
        </div>
      `;
    }).join('');

    this.departuresDiv.innerHTML = html;
  }

  getCardSize() {
    return 3;
  }

  static getConfigElement() {
    return document.createElement('poznan-transport-card-editor');
  }

  static getStubConfig() {
    return {
      entity: '',
      max_departures: 5
    };
  }
}

customElements.define('poznan-transport-card', PoznanTransportCard);

// Make card available in card picker
window.customCards = window.customCards || [];
window.customCards.push({
  type: 'poznan-transport-card',
  name: 'Poznań Transport Card',
  description: 'Display Poznań public transport departures',
  preview: false,
});

console.info(
  '%c POZNAN-TRANSPORT-CARD %c 1.0.0 ',
  'color: white; background: #00aaff; font-weight: 700;',
  'color: #00aaff; background: white; font-weight: 700;'
);

