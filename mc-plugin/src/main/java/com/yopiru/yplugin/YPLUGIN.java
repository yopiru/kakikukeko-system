package com.yopiru.yplugin;

import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.Location;
import org.bukkit.Sound;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.plugin.java.JavaPlugin;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;

import java.io.IOException;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public final class YPLUGIN extends JavaPlugin implements Listener {
    @Override
    public void onEnable() {
        // Plugin startup logic
        getServer().getPluginManager().registerEvents(this, this);
    }

    Integer maintenancelevel = 0;

    // プレイヤーが参加した際にする処理
    @EventHandler
    public void onPlayerJoin(PlayerJoinEvent e) throws IOException {
        if (maintenancelevel == 1){
            Player player = e.getPlayer();
            if (player.getUniqueId().toString().contains("51b9975c-3b0b-4f05-9f0e-32db21b60cd7")){
                player.sendMessage("よし、お前参加おｋ");
            }else {
                player.kickPlayer("プラグインのメンテナンスを開始しました。詳細はDiscordサーバーにて確認してください。");
            }
        }else if (maintenancelevel == 2){
            Player player = e.getPlayer();
            if (player.getUniqueId().toString().contains("51b9975c-3b0b-4f05-9f0e-32db21b60cd7")){
                player.sendMessage("よし、お前参加おｋ");
            }else {
                player.kickPlayer("プラグインの緊急メンテナンスを開始しました。詳細については、Discordサーバーにて、告知される予定です。\n (外部プラグインのメンテナンスなので、長引く可能があります。)");
            }

        }else {
            ObjectMapper objectMapper = new ObjectMapper();
            JsonNode json = objectMapper.readTree(Paths.get("").toFile());
            JsonNode json2 = objectMapper.readTree(Paths.get("").toFile());
            Player player = e.getPlayer();
            String uuid = player.getUniqueId().toString();
            String uuidedit = uuid.replace("-", "");
            List<String> mcidlist = new ArrayList<String>(3);
            List<String> mcidlist2 = new ArrayList<String>(3);
            try {
                int jsonloop = 0;
                while(true){
                    String jsonuuid = json.get(jsonloop).get("uuid").asText();
                    mcidlist.add(jsonuuid);
                    jsonloop = jsonloop + 1;
                }
            } catch (Exception jsonuuid) {
                if (mcidlist.contains(uuidedit)) {
                    player.sendTitle(ChatColor.GOLD + "ようこそ！！", ChatColor.BLUE + "かきくけこ@MCコミュニティへ", 1, 80, 1);
                    Location location = player.getLocation();
                    player.playSound(location, Sound.ENTITY_PLAYER_LEVELUP, 5.0F, 1F);
                    player.playSound(location, Sound.ENTITY_PLAYER_LEVELUP, 5.0F, 1F);
                    return;
                } else {
                    try {
                        int jsonloop2 = 0;
                        while (true){
                            String jsonuuid2 = json2.get(jsonloop2).get("name").asText();
                            mcidlist2.add(jsonuuid2);
                            jsonloop2 = jsonloop2 + 1;
                        }
                    } catch (Exception jsonuuid2) {
                        if (mcidlist2.contains(player.getName())) {
                            player.sendTitle(ChatColor.GOLD + "ようこそ！！", ChatColor.BLUE + "かきくけこ@MCコミュニティへ", 1, 80, 1);
                            Location location = player.getLocation();
                            player.playSound(location, Sound.ENTITY_PLAYER_LEVELUP, 5.0F, 1F);
                            player.playSound(location, Sound.ENTITY_PLAYER_LEVELUP, 5.0F, 1F);
                            return;
                        } else {
                            player.kickPlayer("あなたはサーバー参加登録がされていません、Discordサーバーにて登録してから、もう一度参加してください。");
                        }
                    }


                }
            }
        }
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (label.equalsIgnoreCase("maintenance-mode")) {
            if (args[0].equalsIgnoreCase("0")){
                sender.sendMessage("メンテナンスを開始します。");
                for (Player player : Bukkit.getOnlinePlayers()) {
                    player.kickPlayer("メンテナンスを開始しました。詳細はDiscordサーバーにて確認してください。");
                }
                Bukkit.shutdown();
                return true;
            }
            if (args[0].equalsIgnoreCase("1")) {
                sender.sendMessage("プラグインメンテナンスモードを開始します。");
                maintenancelevel = 1;
                for (Player player : Bukkit.getOnlinePlayers()) {
                    player.kickPlayer("プラグインのメンテナンスを開始しました。詳細はDiscordサーバーにて確認してください。");
                }
                return true;
            } else if (args[0].equalsIgnoreCase("2")) {
                sender.sendMessage("緊急メンテナンスを開始します。");
                for (Player player : Bukkit.getOnlinePlayers()) {
                    player.kickPlayer("緊急メンテナンスを開始しました。詳細については、Discordサーバーにて、告知される予定です。");
                }
                Bukkit.shutdown();
                return true;
            } else if (args[0].equalsIgnoreCase("3")) {
                sender.sendMessage("プラグイン緊急メンテナンスを開始します。");
                for (Player player : Bukkit.getOnlinePlayers()) {
                    player.kickPlayer("プラグインの緊急メンテナンスを開始しました。詳細については、Discordサーバーにて、告知される予定です。\n (外部プラグインのメンテナンスなので、長引く可能があります。)");
                }
                maintenancelevel = 2;
                return true;


            }else if (args[0].equalsIgnoreCase("off")){
                if (maintenancelevel == 0){
                    sender.sendMessage("なんだろう、、、メンテナンスモードじゃないのに、メンテナンスモードOFFにするのやめてもらっていいですか?");
                }else {
                    maintenancelevel = 0;
                    sender.sendMessage("メンテナンスモードをOFFにしました。");
                }
                return true;
            } else {
                sender.sendMessage("有効な数値を入力してください。 \n 入力なし → 通常メンテナンス \n 1番 → プラグインメンテナンス \n 2番 → 緊急メンテナンス \n 3番 → プラグイン緊急メンテナンス");
                return false;
            }
            }
        return false;
    }

    @Override
    public void onDisable() {
        // Plugin shutdown logic
    }
}
