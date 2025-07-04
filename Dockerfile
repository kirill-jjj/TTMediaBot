FROM python:3.11-slim-bookworm
RUN apt update \
    && apt upgrade -y \
    && apt install -y --no-install-recommends \
    gettext \
    libmpv2 \
    p7zip \
    pulseaudio \
    && apt autoclean \
    && apt clean \
    && rm -rf /var/lib/apt/list
RUN pip install uv
RUN useradd -ms /bin/bash ttbot
USER ttbot
WORKDIR /home/ttbot
COPY --chown=ttbot pyproject.toml .
RUN uv sync --system
COPY --chown=ttbot . .
RUN uv run python tools/ttsdk_downloader.py && uv run python tools/compile_locales.py
CMD pulseaudio --start && ./TTMediaBot.sh -c data/config.json --cache data/TTMediaBotCache.dat --log data/TTMediaBot.log
