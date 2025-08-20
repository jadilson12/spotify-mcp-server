# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please send an email to jadilson@example.com. All security vulnerabilities will be promptly addressed.

### What to include in your report:

1. **Description** of the vulnerability
2. **Steps to reproduce** the issue
3. **Potential impact** of the vulnerability
4. **Suggested fix** (if any)

### Security Best Practices

- **Never commit** sensitive files like `.env` to version control
- **Keep your Spotify credentials** secure and private
- **Use environment variables** for all sensitive configuration
- **Regularly update** dependencies to patch security vulnerabilities
- **Follow the principle of least privilege** when configuring Spotify app scopes

### Spotify API Security

This project uses the Spotify Web API. Please ensure:

- Your Spotify app credentials are kept secure
- You use appropriate scopes for your use case
- You follow Spotify's [API Security Guidelines](https://developer.spotify.com/documentation/web-api/security)
- You regularly rotate your client secret if needed

### Environment Variables

Always use environment variables for sensitive data:

```bash
# ✅ Good - Use environment variables
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret

# ❌ Bad - Never hardcode credentials
SPOTIFY_CLIENT_ID=abc123...
```

### Dependencies

We regularly update dependencies to ensure security. To check for vulnerabilities:

```bash
# Install security tools
pip install safety bandit

# Check for known vulnerabilities
safety check

# Run security linter
bandit -r src/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
