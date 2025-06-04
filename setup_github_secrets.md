# GitHub Secrets Setup for AWS Bedrock

To make your newsletter use AWS Bedrock (Anthropic Claude) as the primary LLM with transformer fallback, you need to add these secrets to your GitHub repository:

## Required GitHub Repository Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions → Repository secrets

Add these secrets:

### AWS Bedrock Configuration
```
USE_AWS_BEDROCK=true
AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
AWS_REGION=us-east-1
AWS_BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
```

### LLM Preferences
```
USE_EXTERNAL_LLM=true
PREFERRED_LLM=aws-anthropic
```

### Email Configuration (if not already set)
```
EMAIL_FROM=your-email@example.com
EMAIL_TO=recipient@example.com
EMAIL_USER=your-smtp-username
EMAIL_PASSWORD=your-smtp-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
```

## How to Get AWS Credentials

1. **AWS Console**: Go to AWS IAM → Users → Create User
2. **Permissions**: Attach policy `AmazonBedrockFullAccess` (or create custom policy with bedrock:InvokeModel permission)
3. **Access Keys**: Create access key for the user
4. **Region**: Make sure Bedrock is available in your chosen region (us-east-1 recommended)

## Model Access

Make sure you have access to Claude models in AWS Bedrock:
1. Go to AWS Bedrock console
2. Navigate to "Model access" 
3. Request access to Anthropic Claude models if not already enabled

## Testing

After setting up the secrets, you can test by:
1. Going to Actions tab in your GitHub repository
2. Click "AI Newsletter Daily Scheduler"
3. Click "Run workflow" 
4. Enable "Generate newsletter without sending email" (dry run)
5. Click "Run workflow"

The logs should now show:
```
🤖 Using preferred AWS Bedrock (Anthropic)...
✅ AWS Bedrock generated response successfully
```

Instead of:
```
🔄 Trying transformer model as fallback...
✅ Transformer fallback successful
```

## Fallback Behavior

The system will:
1. **First**: Try AWS Bedrock (Claude) - your preferred option
2. **Fallback**: Use transformer model if Bedrock fails
3. **Last resort**: Try other configured APIs (OpenAI, direct Anthropic)

This ensures your newsletter always generates content even if AWS Bedrock has issues.
