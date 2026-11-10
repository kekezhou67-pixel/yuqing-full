package com.saas.kb.agent.notifier;

import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

@Component
public class AlertNotifier {
    private static final String N8N_WEBHOOK = "http://localhost:5678/webhook/alert";
    private final WebClient webClient = WebClient.create();

    public void sendAlert(String title, String content) {
        webClient.post()
                .uri(N8N_WEBHOOK)
                .bodyValue(java.util.Map.of("title", title, "content", content))
                .retrieve()
                .bodyToMono(String.class)
                .block();
    }
}